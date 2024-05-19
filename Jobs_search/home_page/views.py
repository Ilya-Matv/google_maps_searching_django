from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm


# Create your views here.
def home_page(request):
    return render(request,'main/home.html')

def about_page(request):
    return render(request,'main/about.html')

def contacts_page(request):
    return render(request,'main/contacts.html')

def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,("You have been logged in"))
                return redirect('scrap')
            else:
                messages.success(request,("There was an error, please try again"))
                return redirect('login')
    else:
        return render(request,'main/login.html',{'form':form})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logout"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("You have registered successfully"))
            return redirect('home')
        else:
            messages.success(request,("Woops! there was a problem registering, try again"))
            return redirect('register')
    return render(request, 'main/register.html',{'form':form})
