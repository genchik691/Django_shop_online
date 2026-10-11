# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User  # ✅ Добавьте эту строку


class RegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации отправляет приветственное письмо.
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Сохранение пользователя и отправка приветственного письма."""
        response = super().form_valid(form)
        user = self.object

        # ✅ Отправка приветственного письма
        try:
            send_mail(
                subject='Добро пожаловать в MyShop!',
                message=f'Здравствуйте!\n\n'
                        f'Спасибо за регистрацию в нашем магазине.\n'
                        f'Ваш email: {user.email}\n\n'
                        f'С уважением,\nКоманда MyShop',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"📧 Приветственное письмо отправлено на {user.email}")
        except Exception as e:
            print(f"❌ Ошибка отправки письма: {e}")

        return response


class UserLoginView(LoginView):
    """
    Авторизация по email и паролю.
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        """Перенаправление после успешного входа."""
        return reverse_lazy('catalog:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля пользователя.
    Доступно только авторизованным.
    """
    model = User  # ✅ Теперь User определён
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user

    def form_valid(self, form):
        """Сохранение профиля и вывод сообщения."""
        response = super().form_valid(form)
        print(f"✅ Профиль обновлён: {self.request.user.email}")
        return response

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


from django.shortcuts import render

# Create your views here.
