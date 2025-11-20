from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_signed_up)
def redirect_to_set_user_type(request, user, **kwargs):
    # Allauth does not automatically support redirect here, we handle in `LOGIN_REDIRECT_URL`
    if not (user.is_startup or user.is_investor or user.is_mentor):
        # Store a flag in session to redirect after login
        request.session['needs_user_type'] = True
