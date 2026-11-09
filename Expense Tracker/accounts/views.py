from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Profile


def lg_login(req):

    if req.method == 'POST':

        username = req.POST.get('username', '').strip()
        password = req.POST.get('password', '')

        user = authenticate(
            req,
            username=username,
            password=password
        )

        if user is not None:
            login(req, user)
            return redirect('expenses:transaction-list')

        messages.error(req, 'Username or password is incorrect!')

    return render(req, 'login.html')


def sign_up(req):

    if req.method == 'POST':

        username = req.POST.get('username', '').strip()
        email = req.POST.get('email', '').strip()
        password = req.POST.get('password', '')
        confirm_password = req.POST.get('confirmPassword', '')

        if not username or not password or not confirm_password:
            messages.error(req, 'Please fill in all required fields.')
            return render(req, 'sign-up.html')

        if User.objects.filter(username=username).exists():
            messages.error(req, 'Username already exists.')
            return render(req, 'sign-up.html')

        if email and User.objects.filter(email=email).exists():
            messages.error(req, 'Email already exists.')
            return render(req, 'sign-up.html')

        if password != confirm_password:
            messages.error(req, 'Passwords do not match.')
            return render(req, 'sign-up.html')

        try:
            validate_password(password)
        except ValidationError as errors:
            for error in errors:
                messages.error(req, error)
            return render(req, 'sign-up.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.get_or_create(user=user)

        login(req, user)

        return redirect('expenses:transaction-list')

    return render(req, 'sign-up.html')


def LogOut(req):

    if req.method == 'POST':
        logout(req)

    return redirect('accounts:login')



@login_required(login_url='accounts:login')
def profile(req):
    user = req.user
    profile,credit = Profile.objects.get_or_create(user=user)
    return render(req,'profile.html',{'profile':profile})

# @login_required(login_url='accounts:login')
# def profile(req):

#     user = req.user
#     profile, created = Profile.objects.get_or_create(user=user)

#     return render(req, 'profile.html', {
#         'profile': profile,
#     })