from django import forms
#from .models import User 

class UserForm(forms.Form):
    username = forms.CharField(label='ユーザー名',min_length=5, max_length=20)
    password = forms.CharField(label='パスワード',min_length=5, max_length=20)

class UserUpdateForm(forms.Form):
    username = forms.CharField(label='ユーザー名',min_length=5, max_length=20, required=False)
    password = forms.CharField(label='パスワード',min_length=5, max_length=20, widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label='パスワード（確認用）',min_length=5, max_length=20, widget=forms.PasswordInput(), required=False)

