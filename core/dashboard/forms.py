# Django Imports

from django import forms

# Third Party

from accounts.models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=("first_name", "last_name", "phone_number", "gender")
