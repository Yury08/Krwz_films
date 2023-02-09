from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileImagesForm
from django.contrib.auth.decorators import login_required

from .models import Profile


def register(request):
    if request.method == "POST":  # Получаем данные от позователя
        form = UserRegisterForm(request.POST)  # Хранятся все данные полученные от позователя
        if form.is_valid():  # Проверка данных полученных о пользователя
            form.save()  # Регестрируем пользоваеля в базе данных
            return redirect('home')  # Перебрасываем порльзователя на главную страницу после регистрации
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'title': 'Страница регистрации', 'form': form})


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
        return redirect('profile')
    else:
        instance.profile.save()
