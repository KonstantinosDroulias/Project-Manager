from django import forms
from user.models import UserProfile
import user


class CustomSignupForm(forms.Form):
    avatar = forms.ImageField(label='Profile Picture', required=False)
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )

    def signup(self, request, user):
        """Called after user is created but before saved to handle additional fields """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = UserProfile(user=user)
        profile.avatar = self.cleaned_data.get('avatar')
        profile.save()