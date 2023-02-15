from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    ProfileImagesForm,
                    UserLoginForm)
from django.views.generic.base import (
    TemplateResponseMixin, # Добавит формирование html шаблона и вернёт его в качестве ответа на запрос
    View # Базовый класс для обработчиков django
)
from django.contrib.auth import (
    authenticate,
    login
)


class Login(LoginView, TemplateResponseMixin):
    template_name = 'users/user.html'

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('films:main')
                else:
                    messages.error(request, 'Логин или пароль не корректны')
                    return redirect('user')
            return redirect('films:main')
        return self.render_to_response({'form': form})


def register(request):
    if request.method == "POST":  # Получаем данные от позователя
        form = UserRegisterForm(request.POST)  # Хранятся все данные полученные от позователя
        if form.is_valid():  # Проверка данных полученных о пользователя
            form.save()  # Регестрируем пользоваеля в базе данных
            return redirect('users:user')  # Перебрасываем порльзователя на главную страницу после регистрации
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        profileForm = ProfileImagesForm(request.POST, request.FILES, instance=request.user.profile)
        apdateUserForm = UserUpdateForm(request.POST, instance=request.user)

        if profileForm.is_valid() and apdateUserForm.is_valid():
            apdateUserForm.save()
            profileForm.save()
            return redirect('profile')
    else:
        profileForm = ProfileImagesForm(instance=request.user.profile)
        apdateUserForm = UserUpdateForm(instance=request.user)

    data = {
        'profileForm': profileForm,
        'apdateUserForm': apdateUserForm,
    }

    return render(request, 'users/profile.html', data)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        return redirect('users:user')
    else:
        instance.profile.save()
