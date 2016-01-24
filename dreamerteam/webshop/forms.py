from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    ROLE_CHOICES = (
    ('Customer', 'Customer'),
    ('Developer', 'Developer'),)
    part = forms.ChoiceField(choices = ROLE_CHOICES,required = True, label = 'Role')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self,commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']


        if commit:
            user.save()

        return user
