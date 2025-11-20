from django import forms
from .models import Startup

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['name', 'description', 'industry', 'website', 'location']