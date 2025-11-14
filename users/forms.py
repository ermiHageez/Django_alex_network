# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

USER_TYPES = (
    ('startup', 'Startup'),
    ('investor', 'Investor'),
    ('mentor', 'Mentor'),
)

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
