from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
from django.contrib import messages
from .utils import validate_password
#from django.contrib.auth.decorators import login_required
# Create your views here.


def home_view(request):
    """
    Renders the home page with a welcome message.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: The rendered home page with the context containing the welcome message.
    """
    context = {'message': 'Welcome to the home page!'}
    return render(request, 'home.html', context)

def login_step_1(request):
    """
    View function for the first step of the login process.
    If the request method is POST, it retrieves the email from the request POST data.
    Attempts to retrieve a CustomUser instance based on the provided email.
    If the user exists, renders the 'accounts/password.html' template with the email context.
    If the user does not exist, displays an error message and redirects to the 'login' view.
    If the request method is not POST, renders the 'accounts/login.html' template.

    Parameters:
        request (HttpRequest): The HTTP request object sent by the user.

    Returns:
        HttpResponse: The HTTP response object that either renders a template or redirects the user.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            return render(request, 'accounts/password.html', {'email': email})
        except CustomUser.DoesNotExist:
            messages.error(request, 'Account does not exist.')
            return redirect('login')
    return render(request, 'accounts/login.html')

def login_step_2(request):
    """
    View function for the second step of the login process.
    If the request method is POST, it retrieves the email and password from the request POST data.
    Checks if the password field is missing, displays an error message, and redirects to the 'login' view.
    Attempts to authenticate the user based on the provided email and password.
    If authentication is successful, logs in the user and redirects to the 'home' view.
    If authentication fails, displays an error message and redirects to the 'login_step_2' view.
    If the request method is not POST, redirects to the 'login' view.

    Parameters:
        request (HttpRequest): The HTTP request object sent by the user.

    Returns:
        HttpResponse: The HTTP response object that either redirects the user to different views based on the login process.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not password:
            messages.error(request, 'Password field is missing.')
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')
            return redirect('login_step_2')
    return redirect('login')

def signup(request):
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('signup')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('login')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        try:
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, 'Error creating account')
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')

            



def logout_view(request):
    """
    Logs out the user if the request method is POST and redirects to the home page.

    Parameters:
        request (HttpRequest): The HTTP request object sent by the user.

    Returns:
        HttpResponseRedirect: Redirects the user to the home page after logging out.
    """
    if request.method == 'POST':
        logout(request)
    return redirect('home')