from django.shortcuts import render

from django.contrib import messages
from allauth.account.views import SignupView
from allauth.account import app_settings
# Create your views here.

class CustomSignupView(SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = 'Sign Up'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            messages.info(self.request,
                "We've sent you an email to verify your account. Please Check your inbox."
            )
        else:
            messages.success(self.request,
                f"Welcome {form.cleaned_data.get('username')}. Your account has been created."
            )