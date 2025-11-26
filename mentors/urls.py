from django.urls import path
from .views import MentorsChatView, ListofJoinedStartupsView

urlpatterns = [
    path('joined_startups/', ListofJoinedStartupsView.as_view(), name='joined_startups'),
    path('<int:pk>/chat/', MentorsChatView.as_view(), name='mentor_chat'),
]