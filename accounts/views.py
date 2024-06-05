from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
#from django.contrib.auth.decorators import login_required
# Create your views here.




def login_view(request):
    pass


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')