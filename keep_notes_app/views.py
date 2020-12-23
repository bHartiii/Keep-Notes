from django.shortcuts import HttpResponse, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import CreateUserForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def registration(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)          
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created for '+ user )
                return redirect('login_url')
        context = {'form':form}
        return render(request, 'registration.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('profile')
            
            else:
                messages.info(request, "Username or password is incorrect!!!")
                return render(request, 'login.html')
        return render(request, 'login.html')

@login_required(login_url='login_url')
def profile(request):
    return render(request, 'profile.html')

def logoutUser(request):
    logout(request)
    return redirect('login_url')


