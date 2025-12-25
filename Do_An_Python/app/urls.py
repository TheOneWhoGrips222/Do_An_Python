from django.urls import path
from . import views
from .views import profile
urlpatterns = [
    # Thêm đường dẫn gốc (rỗng) trỏ về home
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('question/<int:id>/', views.question_detail, name='question_detail'),
    path('ask/', views.add_question, name='add_question'),
    path('tags/', views.tags_view, name='tags'),
    path('users/', views.users_view, name='users'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),

    path('profile/', views.profile, name='profile'),
]