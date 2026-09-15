from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
def register(request):
    if request.user.is_authenticated: 
        return redirect('products:home')
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid() :
        login(request,form.save()); 
        messages.success(request,'Account created successfully.'); 
        return redirect('products:home')
    return render(request,'accounts/register.html',{'form':form})

def user_login(request):
    if request.user.is_authenticated: return redirect('products:home')
    form=LoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user()); 
        messages.success(request,'Welcome back!'); 
        return redirect(request.GET.get('next') or 'products:home')
    return render(request,'accounts/login.html', {'form':form})

def user_logout(request):
    logout(request);
    messages.success(request,'You have been logged out.'); 
    return redirect('products:home')
