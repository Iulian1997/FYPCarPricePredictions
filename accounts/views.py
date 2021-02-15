from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        # Get Form Values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Password Validation
        if password == password2:
            # Username Validation
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken!')
                return redirect('register')
            else:
                # Email Validation
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Taken!')
                    return redirect('register')
                else:
                    # All credentials validated
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    
                    # Login after Registration
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in!')
                    # return redirect('index')
                    user.save()
                    messages.success(request, ': Registered Successfully! You can now login.')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Login User
        return
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')