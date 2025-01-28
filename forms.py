from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tournament, UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TournamentForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Дата начала'}),
        label='Дата начала'
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Дата окончания'}),
        label='Дата окончания'
    )
    registration_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Дедлайн регистрации'}),
        label='Дедлайн регистрации'
    )
    # date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    #     label='Дата проведения'
    # )

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'start_date', 'end_date', 'registration_deadline', 'description', 'status', 'max_participants', 'organization_name', 'company_info', 'first_name', 'last_name', 'address', 'postal_code', 'city', 'country', 'email', 'phone_number', 'image']
        labels = {
            'name': 'Название турнира',
            'location': 'Место проведения',
            'description': 'Описание',
            'type': 'Тип турнира',
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание турнира'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите место проведения'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название турнира'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        label='Пароль'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}),
        label='Подтвердите пароль'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Электронная почта'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture'] 