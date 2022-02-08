from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
import requests
from dashboard.models import Favourites

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
                    # Save new user
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
        # Get Form Values
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        # Login Validation
        if user is not None:
            auth.login(request, user)
            messages.success(request, ': You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong Credentials!')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # Logout
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, ': You are now logged out!')
        return redirect('index')

def dashboard(request):
    if request.method == 'POST':
        # Get Form Values
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        transmission = request.POST['transmission']
        mileage = request.POST['mileage']
        tax = float(request.POST['tax'])
        mpg = float(request.POST['mpg'])
        engine_size = request.POST['engine_size']
        price = request.POST['price']

        # Setting current user
        current_user = request.user

        # Adding prediction prices with values to Favourites
        newFavourite = Favourites(user = current_user, make=make, model=model, year=year, transmission=transmission, mileage=mileage, tax=tax, mpg=mpg, engine_size=engine_size, price=price)
        newFavourite.save()

        messages.success(request, ': Added to Dashboard!')

    current_user = request.user

    listOfFavourites = Favourites.objects.filter(user = current_user)

    context = {
        'fav':listOfFavourites
    }

    return render(request, 'accounts/dashboard.html', context)