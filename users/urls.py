from django.urls import path
from .views import (
    RegisterView, LoginView, DashboardView, HomeView,
    StartupDashboardView, InvestorDashboardView, MentorDashboardView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('startup/', StartupDashboardView.as_view(), name='startup_dashboard'),
    path('investor/', InvestorDashboardView.as_view(), name='investor_dashboard'),
    path('mentor/', MentorDashboardView.as_view(), name='mentor_dashboard'),
]
