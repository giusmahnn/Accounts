from django.urls import path
from .views import logout_view, login_step_1, login_step_2, signup

urlpatterns = [
    path('login/', login_step_1, name='login'),
    path('login-step-2/', login_step_2, name='login_step_2'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
]