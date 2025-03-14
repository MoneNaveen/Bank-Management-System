from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name','mobile','email','aadhar','father_name','dob','gender','photo','address','state','balance']
class Recaptcha(forms.Form):
    captcha = ReCaptchaField()