from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Thêm đường dẫn gốc (rỗng) trỏ về home
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('quest/', views.question_page, name="quest-page"),
    path('question/<int:id>/', views.question_detail, name='question_detail'),
    path('ask/', views.add_question, name='add_question'),
    path('tags/', views.tags_view, name='tags'),
    path('users/', views.users_view, name='users'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),

    # 2. Thông báo "Đã gửi email"
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    # 3. Trang nhập mật khẩu mới (Link từ email trỏ về đây)
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # 4. Thông báo "Đổi mật khẩu thành công"
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('api/search_similar/', views.search_similar_questions, name='search_similar_questions'),

    path('answer/<int:id>/', views.accept_answer, name='accept_answer'),
]