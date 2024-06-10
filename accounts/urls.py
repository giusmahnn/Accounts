from django.urls import path
from .views import (logout_view, 
                    login_step_1, 
                    login_step_2, 
                    signup, 
                    profile, 
                    profile_edit, 
                    change_password,
                    )

urlpatterns = [
    path('login/', login_step_1, name='login'),
    path('login-step-2/', login_step_2, name='login_step_2'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile-edit/', profile_edit, name='profile_edit'),
    path('change-password/', change_password, name='change_password'),
    path('logout/', logout_view, name='logout'),
]