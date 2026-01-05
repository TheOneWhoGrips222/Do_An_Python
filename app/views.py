from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Question, Answer, Tag
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse

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
    tags = Tag.objects.annotate(num_questions=Count('questions')).order_by('-num_questions')
    return render(request, 'app/tag.html', {'tags': tags})

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

def search_similar_questions(request):
    """API trả về JSON danh sách câu hỏi tương tự cho tính năng Autocomplete"""
    query = request.GET.get('q', '')
    if len(query) > 2:
        # Tìm các câu hỏi có tiêu đề chứa từ khóa (không phân biệt hoa thường)
        questions = Question.objects.filter(title__icontains=query)[:5]
        results = []
        for q in questions:
            results.append({
                'title': q.title,
                'url': reverse('question_detail', args=[q.id]), # Tạo link đến câu hỏi đó
                'answers': q.answers.count() # Số câu trả lời hiện có
            })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})