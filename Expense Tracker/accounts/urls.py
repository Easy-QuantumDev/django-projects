from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
path('login/', views.lg_login, name='login'),
path('signup/', views.sign_up, name='sign-up'),
path('logout/', views.LogOut, name='logout'),    
path("profile/",views.profile , name = 'profile')
]
