from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Startup
from .forms import StartupForm
# Create your views here.
# List of Startups
class StartupListView(ListView):
    model = Startup
    template_name = 'startups/startup_list.html'
    context_object_name = 'startups'
    ordering = ['-created_at']
    paginate_by = 10

# View details of a specific Startup
class StartupDetailView(DetailView):
    model = Startup
    template_name = 'startups/startup_detail.html'
    context_object_name = 'startup'

# Create a new Startup
class StartupCreateView(LoginRequiredMixin, CreateView):
    model = Startup
    form_class = StartupForm
    template_name = 'startups/startup_form.html'
  
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Startup created successfully!')
        return response
    def get_success_url(self):
        return reverse_lazy('startup-detail', kwargs={'pk': self.object.pk})
    
# Update an existing Startup

class StartupUpdateView(LoginRequiredMixin, UpdateView):
    model = Startup
    form_class = StartupForm
    template_name = 'startups/startup_form.html'

    def get_queryset(self):
        # Only allow owners to update their startups
        return Startup.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Startup updated successfully!')
        return response
    def get_success_url(self):
        return reverse_lazy('startup_detail', kwargs={'pk': self.object.pk})