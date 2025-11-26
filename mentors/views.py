from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from mentors.models import ChatMessage, Mentor
from users.models import User
from startups.models import Startup

# Create your views here.

# class ListofDashboardView(LoginRequiredMixin, ListView):
#     model = Startup
#     template_name = 'users/mentor_dashboard.html'
#     context_object_name = 'startups'

#     def get_queryset(self):
#         return Startup.members.all()


# class ListofJoinedStartupsView(LoginRequiredMixin, TemplateView):
#     template_name = 'mentors/joined_startups.html'
    
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         mentor = getattr(self.request.user, 'mentor_profile', None)
#         if mentor is None:
#             ctx['startups'] = []
#         else:
#             # Mentor model defines a ManyToManyField named `startups`
#             ctx['startups'] = mentor.startups.all()
#         return ctx



class ListofJoinedStartupsView(LoginRequiredMixin, ListView):
    model = Startup
    template_name = 'mentors/joined_startups.html'
    context_object_name = 'startups'

    def get_queryset(self):
        mentor = getattr(self.request.user, 'mentor_profile', None)
        if mentor is None:
            try:
                mentor = Mentor.objects.get(user=self.request.user)
            except Exception:
                mentor = None

        if mentor is None:
            return Startup.objects.none()

        return mentor.startups.all()


class MentorsChatView(LoginRequiredMixin, TemplateView):
    template_name = 'mentors/mentor_chat.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        mentor = None
        try:
            mentor = Mentor.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            mentor = None

        ctx['mentor'] = mentor

        if mentor is not None:
            startup_pks = mentor.startups.values_list('pk', flat=True)
        
            try:
                msgs = ChatMessage.objects.filter(Mentor_id__in=list(startup_pks)).select_related('sender')
            except Exception:
                msgs = ChatMessage.objects.none()
        else:
            msgs = ChatMessage.objects.none()

        ctx['messages'] = msgs
        return ctx