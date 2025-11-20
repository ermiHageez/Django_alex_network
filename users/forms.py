from django import forms
from .models import User

# Existing CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm

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


# New form for social login user type selection
class SocialUserTypeForm(forms.Form):
    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.RadioSelect,
        label="I am a"
    )
