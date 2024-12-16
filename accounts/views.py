from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm

class RegisterView(View):
    def get(self, request):
        """
        Renders the registration form for unauthenticated users.

        :param request: The request
        :return: The response
        """
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        """
        Processes the registration form, logs the user in and redirects to the news list
        on success, or renders the registration form with errors on failure.

        :param request: The request
        :return: The response
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('news_list')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        """
        Renders the login form for unauthenticated users.

        :param request: The request
        :return: The response
        """
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        """
        Processes the login form, authenticates the user and redirects to the news list
        on success, or renders the login form with errors on failure.

        :param request: The request
        :return: The response
        """

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли!")
            return redirect('news_list')
        return render(request, 'accounts/login.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        """
        Logs the user out, displays a success message and redirects to the news list.

        :param request: The request
        :return: The response
        """
        logout(request)
        messages.success(request, "Вы вышли из системы.")
        return redirect('news_list')

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        """
        Renders the password change form for the current user.

        :param request: The request
        :return: The response
        """
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    def post(self, request):
        """
        Processes the password change form, changes the password and redirects to the news list
        on success, or renders the password change form with errors on failure.

        :param request: The request
        :return: The response
        """
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пароль успешно изменён!")
            return redirect('news_list')
        return render(request, 'accounts/change_password.html', {'form': form})
