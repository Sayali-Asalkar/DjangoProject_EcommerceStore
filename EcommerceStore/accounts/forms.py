from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'})); 
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User; 
        fields=['username','email']; 
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),'email':forms.EmailInput(attrs={'class':'form-control'})}
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists(): raise forms.ValidationError('Username already exists.')
        return username
    
    def clean(self):
        data=super().clean()
        if data.get('password') and data.get('confirm_password') and data['password']!=data['confirm_password']: self.add_error('confirm_password','Passwords do not match.')
        return data
    
    def save(self,commit=True):
        user=super().save(commit=False); 
        user.set_password(self.cleaned_data['password'])
        if commit: user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})); 
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
