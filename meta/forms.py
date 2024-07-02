from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class myForm(forms.Form):
    file = forms.FileField(
        label='Image',
        #widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    caption = forms.CharField(
        label='Caption',
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'rows': 4, 
                'cols': 40,
                'placeholder': 'Enter your caption here...',
            }
    ))

class storyForm(forms.Form):
    file = forms.FileField(
        label='Image',
    )

class formSet(forms.Form):
    email = forms.EmailField(label='Email')
    slToken = forms.CharField(label='Access Token', max_length=300)
    fbPgId = forms.IntegerField(label='FB Page ID')
    appId = forms.IntegerField(label='App ID')
    appSecret = forms.CharField(label='App Secret',max_length=150)

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileCaro(forms.Form):
    images = MultipleFileField()
    caption = forms.CharField(
        label='Caption',
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'rows': 4, 
                'cols': 40,
                'placeholder': 'Enter your caption here...',
            }
    ))

class FBText(forms.Form):
    text = forms.CharField(
        label='Message',
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'rows': 6, 
                'cols': 40,
                'placeholder': 'Enter your caption here...',
            }
    ))

#---register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#---login
class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())