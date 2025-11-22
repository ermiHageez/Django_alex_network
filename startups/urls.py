from django.urls import path
from .views import (
    StartupListView,
    StartupCreateView,
    StartupUpdateView,
    StartupDetailView,
    StartupMemberDetailView, 
    StartupChatView,
)

urlpatterns = [
    path('', StartupListView.as_view(), name='startup_list'),
    path('create/', StartupCreateView.as_view(), name='startup_create'),
    path('<int:pk>/', StartupDetailView.as_view(), name='startup_detail'),
    path('<int:pk>/chat', StartupChatView.as_view(), name='startup_chat'),
    path('update/<int:pk>/', StartupUpdateView.as_view(), name='update_startup'),
    path('member/<int:pk>/', StartupMemberDetailView.as_view(), name='startup_member_detail'), 
]