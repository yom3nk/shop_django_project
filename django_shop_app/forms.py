from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product

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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Nazwa kategorii',
        }

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Kategoria')
    
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']
        labels = {
            'name': 'Nazwa produktu',
            'description': 'Opis produktu',
            'price': 'Cena',
            'image': 'Obraz produktu',
        }