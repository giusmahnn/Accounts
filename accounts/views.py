from django.forms import ValidationError
from django.shortcuts import  render,redirect
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
from django.contrib import messages
from .utils import validate_password
from django.contrib.auth.decorators import login_required
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
    """
    Handles the user signup process.

    If the request method is POST, it retrieves the username, email, password, and confirm_password from the request POST data.
    Validates the password and checks if the password and confirm_password match.
    Checks if the username or email already exists in the database.
    If all validations pass, creates a new CustomUser instance, sets the password, saves the user, logs in the user, and redirects to the home page.
    If any validation fails, displays an error message and redirects to the signup view.
    If the request method is not POST, renders the signup template.

    Parameters:
        request (HttpRequest): The HTTP request object sent by the user.

    Returns:
        HttpResponse: The HTTP response object that either redirects the user to different views based on the signup process or renders the signup template.
    """
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
            return redirect('signup')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists, Please login')
            return redirect('login')
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/signup.html')


def profile(request):
    """
    Renders the profile page for the authenticated user.

    Parameters:
        request (HttpRequest): The HTTP request object sent by the user.

    Returns:
        HttpResponse: The rendered profile page with the context containing the authenticated user information.
    """
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required(login_url='login')
def profile_edit(request):
    """
    Handles the user profile editing process.

    This function is decorated with @login_required to ensure that only authenticated users can access this view.
    If the request method is GET, it retrieves the authenticated user's information and renders the 'accounts/edit_profile.html' template with the user's information.
    If the request method is POST, it retrieves the updated bio, location, and date_of_birth from the request POST data.
    Updates the authenticated user's information with the new values, saves the changes, and displays a success message.
    Finally, redirects the user to the 'profile' view.

    Parameters:
    request (HttpRequest): The HTTP request object sent by the user.

    Returns:
    HttpResponse: The HTTP response object that either renders the edit profile template or redirects the user to different views based on the request method.
    """
    if request.method == 'GET':
        user = request.user
        return render(request, 'accounts/edit_profile.html', {'user': user})
    elif request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        date_of_birth = request.POST.get('date_of_birth')
        user = request.user
        user.bio = bio
        user.location = location
        user.date_of_birth = date_of_birth
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    



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