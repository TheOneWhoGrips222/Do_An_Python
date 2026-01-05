from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Question, Answer, Vote
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction


User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email")

def home(request):
    questions = Question.objects.all().order_by('-creation_date')
    context = {
        'questions': questions
    }
    return render(request, 'app/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def question_detail(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        content = request.POST.get('content')
        if content:
            Answer.objects.create(
                question=question,
                body=content,
                own_user=request.user
            )
            return redirect('question_detail', id=id)
    return render(request, 'app/question.html', {'question': question})

def add_question(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        if title and body:
            Question.objects.create(
                title=title,
                body=body,
                own_user=request.user
            )
            return redirect('home')
    return render(request, 'app/AddQuestion.html')

def tags_view(request):
    return render(request, 'app/tag.html')

def users_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'app/user.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_questions = Question.objects.filter(own_user=user).order_by('-creation_date')
    context = {
        'profile_user': user,
        'user_questions': user_questions
    }
    return render(request, 'app/ManageUser.html', context)

def question_page(request):
    questions = Question.objects.all().order_by('creation_date').prefetch_related('tags')
    user_count = User.objects.all().count()
    question_count = Question.objects.all().count()
    context = {'questions': questions,
               'user_count': user_count,
               'question_count': question_count
               }

    return render(request, 'app/question-list.html',context)
@login_required
@require_POST
def vote_question(request, id):
    q = get_object_or_404(Question, id=id)

    # Không cho tự vote bài mình (đỡ bị thầy hỏi “lách điểm”)
    if q.own_user_id == request.user.id:
        return redirect(request.META.get("HTTP_REFERER", "quest-page"))

    try:
        value = int(request.POST.get("value"))
    except (TypeError, ValueError):
        return redirect(request.META.get("HTTP_REFERER", "quest-page"))

    if value not in (1, -1):
        return redirect(request.META.get("HTTP_REFERER", "quest-page"))

    # Luật reputation cho vote câu hỏi
    REP_MAP = {1: 5, -1: -2}

    with transaction.atomic():
        existing = Vote.objects.filter(user=request.user, question=q).first()

        if existing is None:
            # Tạo vote mới
            Vote.objects.create(user=request.user, question=q, value=value)
            q.score += value
            q.save(update_fields=["score"])

            owner = q.own_user
            owner.reputation += REP_MAP[value]
            owner.save(update_fields=["reputation"])

        else:
            if existing.value == value:
                # Bấm lại -> gỡ vote
                existing.delete()
                q.score -= value
                q.save(update_fields=["score"])

                owner = q.own_user
                owner.reputation -= REP_MAP[value]
                owner.save(update_fields=["reputation"])

            else:
                # Đổi vote (ví dụ -1 -> +1)
                old_value = existing.value
                existing.value = value
                existing.save(update_fields=["value"])

                # score đổi theo chênh lệch
                q.score += (value - old_value)
                q.save(update_fields=["score"])

                # reputation đổi theo chênh lệch
                owner = q.own_user
                owner.reputation += (REP_MAP[value] - REP_MAP[old_value])
                owner.save(update_fields=["reputation"])

    return redirect(request.META.get("HTTP_REFERER", "quest-page"))
