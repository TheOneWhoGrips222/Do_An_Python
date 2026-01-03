from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms  # Import thêm thư viện forms
from .models import Question, Answer


# --- 1. TẠO FORM ĐĂNG KÝ CÓ EMAIL ---
class SignUpForm(UserCreationForm):
    # Thêm trường email, bắt buộc nhập
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        # Các trường sẽ lưu vào database (Lưu ý: password đã được UserCreationForm tự xử lý)
        fields = ("username", "email")


# --- 2. CÁC VIEW ---

def home(request):
    questions = Question.objects.all().order_by('-CreationDate')
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
        # Sử dụng form SignUpForm vừa tạo ở trên thay vì UserCreationForm cũ
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
                AnswerBody=content,
                OwnUser=request.user
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
                Title=title,
                Body=body,
                OwnUser=request.user
            )
            return redirect('home')

    return render(request, 'app/AddQuestion.html')


# --- Các view phụ ---
def tags_view(request):
    return render(request, 'app/tag.html')


def users_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'app/user.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_questions = Question.objects.filter(OwnUser=user).order_by('-CreationDate')
    context = {
        'profile_user': user,
        'user_questions': user_questions
    }
    return render(request, 'app/ManageUser.html', context)