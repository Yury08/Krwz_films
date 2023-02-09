from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('reg/', user_views.register, name='reg'),
    path('profile/', user_views.profile, name='profile'),
    path('exit/', auth_views.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('pass-reset/', auth_views.PasswordResetView.as_view(template_name='users/pass_reset.html'), name='pass-reset'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users'
                                                                                                '/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users'
                                                                                                               '/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
]
