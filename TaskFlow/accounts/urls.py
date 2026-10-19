from django.urls import path 
from .views import loginView,signup,logoutView
app_name = 'accounts'
urlpatterns = [
    path("login/",loginView,name='login-page'),
    path("logout/",logoutView,name='logout-page'),
    path("signup/",signup,name='signup-page'),
    
    
]
