from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        # ДОБАВЬ ЭТОТ КУСОК КОДА 👇
        from django.core.mail import send_mail
        from django.conf import settings

        send_mail(
            subject='Добро пожаловать в SkyStore!',
            message=f'Привет, {user.email}! Ты зарегился, красава! 🍻',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        login(self.request, user, backend='users.backends.EmailBackend')
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')  # Явно указываем куда перенаправлять после входа

    def form_valid(self, form):
        print("=== ДЕБАГ ФОРМЫ ВХОДА ===")
        print(f"Данные формы: {form.cleaned_data}")

        # Проверяем аутентификацию вручную
        from django.contrib.auth import authenticate
        user = authenticate(
            email=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        print(f"Authenticate вернул: {user}")
        print(f"User is_authenticated: {user.is_authenticated if user else 'None'}")

        return super().form_valid(form)

    def form_invalid(self, form):
        print("=== ФОРМА НЕВАЛИДНА ===")
        print(f"Ошибки: {form.errors}")
        return super().form_invalid(form)

def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'avatar', 'phone', 'country']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


def simple_login(request):
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Пытаемся войти: {email} / {password}")

        user = authenticate(email=email, password=password)
        print(f"Authenticate result: {user}")

        if user:
            login(request, user)
            print("Успешный вход!")
            return redirect('home')
        else:
            print("Ошибка входа!")
            return render(request, 'users/simple_login.html', {'error': 'Неверные данные'})

    return render(request, 'users/simple_login.html')