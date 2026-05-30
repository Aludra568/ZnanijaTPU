from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150, 
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте логин'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Минимум 8 символов'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Минимум 8 символов'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control ко всем полям
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # Подсказка из label
            
        # Убираем лишнюю помощь (можно оставить, если нужно)
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''

    

# class VerifyCodeForm(forms.Form):
#     code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
#         'class': 'form-control text-center fs-3 fw-bold',
#         'placeholder': '••••••',
#         'maxlength': '6',
#         'pattern': '[0-9]{6}',
#         'inputmode': 'numeric'
#     }))

# class LoginUserForm(forms.Form):
#     username = forms.CharField(label='Логин', 
#             widget=forms.TextInput(attrs={'class': 'form-input'}))
    
#     password = forms.CharField(label='Пароль', 
#             widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    