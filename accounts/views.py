from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

class HomeView(TemplateView):
    template_name = "home.html"

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"

class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Registration successful! 🎉")
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        messages.success(self.request, "You are now logged in ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid credentials ❌")
        return super().form_invalid(form)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("accounts:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out 👋")
        return super().dispatch(request, *args, **kwargs)
