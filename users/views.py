from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm
from startups.models import Startup
from mentors.models import Mentor
from investors.models import Investor


# -----------------------
# Registration CBV
# -----------------------
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user_type = self.request.POST.get('user_type')

        # Assign user type flags
        if user_type == 'startup':
            user.is_startup = True
        elif user_type == 'investor':
            user.is_investor = True
        elif user_type == 'mentor':
            user.is_mentor = True

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
    login_url = '/login/'
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
            return redirect('home')


# -----------------------
# Home page CBV
# -----------------------
class HomeView(TemplateView):
    template_name = 'users/home.html'


# -----------------------
# Startup dashboard (with startup list)
# -----------------------
class StartupDashboardView(LoginRequiredMixin, ListView):
    model = Mentor
    template_name = 'users/startup_dashboard.html'
    context_object_name = 'mentors'

    def get_queryset(self):
        return Mentor.objects.all()


# -----------------------
# Investor dashboard
# -----------------------
class InvestorDashboardView(LoginRequiredMixin, ListView):
    model = Investor
    template_name = 'users/investor_dashboard.html'
    context_object_name = 'investors'

    def get_queryset(self):
        return Investor.objects.all()


# -----------------------
# Mentor dashboard
# -----------------------
class MentorDashboardView(LoginRequiredMixin, ListView):
    model = Startup
    template_name = 'users/mentor_dashboard.html'
    context_object_name = 'startups'

    def get_queryset(self):
        return Startup.objects.all()


# -----------------------
# Join Views (Functions)
# -----------------------
def join_startup(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    messages.success(request, f"You’ve requested to join {startup.name}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def join_investor(request, investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    messages.success(request, f"You’ve requested to connect with investor {investor.name}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def join_mentor(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    messages.success(request, f"You’ve requested mentorship from {mentor.user}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
