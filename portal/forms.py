

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StaffProfile

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username","email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "Password*"
        #for fieldname in ['username','email' ,'password1', 'password2']:
         #   self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        
        user.is_active = True
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ('company','address','city','country','postal_code')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
