from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST

def loginView(req):
    if req.method == 'POST':
        username = req.POST.get("username")
        password = req.POST.get("password")
        user = authenticate(username = username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req, "You logged in successfully!")
            return redirect('tasks:home')
        messages.error(req, "Invalid username or password.")
    return render(req,"login.html")



def signup(req):
    
    if req.method == 'POST':
        
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req,user)
            messages.success(req, "Your account was created successfully!")
            return redirect("tasks:home")
    else:
        form = UserCreationForm()
            
    return render(req,'signup.html',{'form':form})
    
    
@require_POST    
def logoutView(req):
    logout(req)
    messages.success(req, "You logged out successfully!")
    return redirect("tasks:home")        

                


# Create your views here.
