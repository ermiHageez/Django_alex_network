# users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm

# -----------------------
# Registration CBV
# -----------------------
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Save the user without committing yet
        user = form.save(commit=False)

        # Assign user type from radio buttons
        user_type = self.request.POST.get('user_type')
        if user_type == 'startup':
            user.is_startup = True
        elif user_type == 'investor':
            user.is_investor = True
        elif user_type == 'mentor':
            user.is_mentor = True

        # Save user and login
        user.save()
        login(self.request, user)

        return super().form_valid(form)

# -----------------------
# Login CBV
# -----------------------
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

# -----------------------
# Dashboard CBV with redirection
# -----------------------
class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'  # redirect if not logged in
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_startup:
            return redirect('startup_dashboard')
        elif user.is_investor:
            return redirect('investor_dashboard')
        elif user.is_mentor:
            return redirect('mentor_dashboard')
        else:
            return redirect('home')  # fallback

# -----------------------
# Home page CBV
# -----------------------
class HomeView(TemplateView):
    template_name = 'users/home.html'
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Startup dashboard
class StartupDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/startup_dashboard.html'

# Investor dashboard
class InvestorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/investor_dashboard.html'

# Mentor dashboard
class MentorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/mentor_dashboard.html'
