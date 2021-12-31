from django import forms
from django.forms import fields
from .models import Document, User

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["file"]

    # def save(self, commit: bool):
        
    #     return super().save(commit=commit)

class RegisterForm(forms.ModelForm):
    username=forms.CharField(max_length=100,label="Kullanıcı Adı")
    password1=forms.CharField(max_length=100,label="Parola",widget=forms.PasswordInput)
    password2=forms.CharField(max_length=100,label="Parola",widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=[
            'username',
            'password1',
            'password2',
        ]
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError('Parolalar aynı değil')
        return password2       