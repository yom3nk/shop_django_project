from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):   
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None 
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Potwierdź hasło'