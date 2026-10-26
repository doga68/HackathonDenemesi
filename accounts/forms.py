from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    company_name = forms.CharField(label='Otel / Şirket adı', required=False)
    skills = forms.CharField(label='Nitelikler (virgülle ayırın: garson, almanca, resepsiyon)', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'phone']
