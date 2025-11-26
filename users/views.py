from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, SocialUserTypeForm
from startups.models import Startup
from mentors.models import Mentor
from investors.models import Investor


# -----------------------------------------------------
# Registration (CBV)
# -----------------------------------------------------
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user_type = self.request.POST.get('user_type')

        # Assign user type flag
        if user_type == 'startup':
            user.is_startup = True
        elif user_type == 'investor':
            user.is_investor = True
        elif user_type == 'mentor':
            user.is_mentor = True

        user.save()
        login(self.request, user)
        return super().form_valid(form)


# -----------------------------------------------------
# Login (CBV)
# -----------------------------------------------------
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


# -----------------------------------------------------
# Dashboard Redirect Logic
# -----------------------------------------------------
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
            # If no type is set yet (e.g., social login)
            return redirect('set_user_type')


# -----------------------------------------------------
# Home Page
# -----------------------------------------------------
class HomeView(TemplateView):
    template_name = 'users/home.html'


# -----------------------------------------------------
# Startup Dashboard (Shows mentors)
# -----------------------------------------------------
class StartupDashboardView(LoginRequiredMixin, ListView):
    model = Mentor
    template_name = 'users/startup_dashboard.html'
    context_object_name = 'mentors'

    def get_queryset(self):
        return Mentor.objects.all()


# -----------------------------------------------------
# Investor Dashboard (Shows investors)
# -----------------------------------------------------
class InvestorDashboardView(LoginRequiredMixin, ListView):
    model = Investor
    template_name = 'users/investor_dashboard.html'
    context_object_name = 'investors'

    def get_queryset(self):
        return Investor.objects.all()


# -----------------------------------------------------
# Mentor Dashboard (Shows startups)
# -----------------------------------------------------
class MentorDashboardView(LoginRequiredMixin, ListView):
    model = Startup
    template_name = 'users/mentor_dashboard.html'
    context_object_name = 'startups'

    def get_queryset(self): 
        return Startup.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            joined_ids = set(Startup.objects.filter(members=self.request.user).values_list('id', flat=True))
        except Exception:
            joined_ids = set()
        ctx['joined_startup_ids'] = joined_ids
        return ctx


# -----------------------------------------------------
# Join Views (CBV)
# -----------------------------------------------------
@method_decorator(login_required, name='dispatch')
class JoinStartupView(View):
    def post(self, request, startup_id):
        startup = get_object_or_404(Startup, id=startup_id)

        if request.user in startup.members.all():
            messages.warning(request, f"You are already a member of {startup.name}.")
        else:
            startup.members.add(request.user)
            messages.success(request, f"You’ve successfully joined {startup.name}!")

        return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator(login_required, name='dispatch')
class JoinInvestorView(View):
    def post(self, request, investor_id):
        investor = get_object_or_404(Investor, id=investor_id)

        # You can add connection request logic here later
        messages.success(request, f"You’ve requested to connect with investor {investor.name}.")

        return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator(login_required, name='dispatch')
class JoinMentorView(View):
    def post(self, request, mentor_id):
        mentor = get_object_or_404(Mentor, id=mentor_id)

        # You can add mentorship request logic here later
        messages.success(request, f"You’ve requested mentorship from {mentor.user}.")

        return redirect(request.META.get('HTTP_REFERER', '/'))


# -----------------------------------------------------
# Social login user type selection
# -----------------------------------------------------
@login_required
def set_user_type(request):
    user = request.user
    if user.is_startup or user.is_investor or user.is_mentor:
        # Already set, redirect to dashboard
        return redirect('dashboard')

    if request.method == "POST":
        form = SocialUserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user.is_startup = user_type == 'startup'
            user.is_investor = user_type == 'investor'
            user.is_mentor = user_type == 'mentor'
            user.save()
            return redirect('dashboard')
    else:
        form = SocialUserTypeForm()

    return render(request, 'users/set_user_type.html', {'form': form})
