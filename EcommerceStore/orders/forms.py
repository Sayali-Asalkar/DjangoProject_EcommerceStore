from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order; 
        fields=['full_name','email','phone','address','city','pincode']
        widgets={f:forms.TextInput(attrs={'class':'form-control'}) for f in ['full_name','email','phone','city','pincode']}
        widgets['email']=forms.EmailInput(attrs={'class':'form-control'});
        widgets['address']=forms.Textarea(attrs={'class':'form-control','rows':3})
