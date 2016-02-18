from django import forms
from django.conf import settings
from webshop.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required = True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get['username']
        password = self.cleaned_data.get['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')
        if not user.is_active:
            raise forms.ValidationError('Login failed. Your account is inactive')
            
    def login(self, request):
        username = self.cleaned_data.get['username']
        password = self.cleaned_data.get['password']
        user = authenticate(username=username, password=password)
        return user

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    ROLE_CHOICES = (
    ('Customer', 'Customer'),
    ('Developer', 'Developer'),)
    group = forms.ChoiceField(choices = ROLE_CHOICES,required = True, label = 'Role')

    class Meta:
        model = User
        #fields = ('username','email', 'password1', 'password2')
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')

    def save(self,commit = True):
        user = super(RegistrationForm, self).save(commit = False)
        user.save()
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()
        return user

class GameForm(forms.ModelForm):
    published = forms.DateField( widget=forms.DateInput(attrs={'class': 'form-control'}), localize=True) # should be formatted to finnish format?

    class Meta:
        model = Game
        fields = ['name', 'price', 'url', 'published', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'})
        }
