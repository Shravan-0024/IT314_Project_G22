from django.shortcuts import render,redirect
from app_home.forms import UserSignUpForm,UserProfileEditForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Notify
from .forms import NotifyForm,FeedbackForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
import requests
from datetime import datetime

API_KEY = '3fd909629968761c4f36f936ba57ef90'

def home_view(request):
    if request.method == "POST":
        city = request.POST["location"]
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

        response = requests.get(url)
        data = response.json()
        # allowing user to access home page even if he is logged in - Consider it as feature
        if response.status_code == 200:
            print(data)
            # Extract sunrise and sunset timestamps and convert them
            sunrise_timestamp = data['sys']['sunrise']
            sunset_timestamp = data['sys']['sunset']
            sunrise = datetime.fromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            sunset = datetime.fromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Add the formatted timestamps to the context
            
            return render(request,'home/home.html',{'sunrise': sunrise,
                'sunset': sunset,"data":data})
        else:
            return render(request,'home/home.html',{"error":f"Some Error Occured for '{city}' \nCurrently we are unable to serve you"})
        
    else:
        city1 = 'Delhi'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city1}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data_Delhi = response.json()
        sunrise_timestamp_d = data_Delhi['sys']['sunrise']
        sunset_timestamp_d = data_Delhi['sys']['sunset']
        sunrise_d = datetime.fromtimestamp(sunrise_timestamp_d).strftime('%Y-%m-%d %H:%M:%S')
        sunset_d = datetime.fromtimestamp(sunset_timestamp_d).strftime('%Y-%m-%d %H:%M:%S')
        city2 = 'Mumbai'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city2}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data_Mumbai = response.json()
        sunrise_timestamp_m = data_Mumbai['sys']['sunrise']
        sunset_timestamp_m = data_Mumbai['sys']['sunset']
        sunrise_m = datetime.fromtimestamp(sunrise_timestamp_m).strftime('%Y-%m-%d %H:%M:%S')
        sunset_m = datetime.fromtimestamp(sunset_timestamp_m).strftime('%Y-%m-%d %H:%M:%S')
        city3 = 'Hyderabad'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city3}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data_Hyderabad = response.json()
        sunrise_timestamp_h = data_Hyderabad['sys']['sunrise']
        sunset_timestamp_h = data_Hyderabad['sys']['sunset']
        sunrise_h = datetime.fromtimestamp(sunrise_timestamp_h).strftime('%Y-%m-%d %H:%M:%S')
        sunset_h = datetime.fromtimestamp(sunset_timestamp_h).strftime('%Y-%m-%d %H:%M:%S')
        if response.status_code == 200:
            return render(request,'home/home.html', {'data_Delhi': data_Delhi,
                'data_Mumbai': data_Mumbai,"data_Hyderabad":data_Hyderabad, 'sunrise_d': sunrise_d,
                'sunset_d': sunset_d, 'sunrise_m': sunrise_m, 'sunset_m': sunset_m, 'sunrise_h': sunrise_h,
                'sunset_h': sunset_h })
    
def dashboard_view(request):
    if request.method == "POST":
        city = request.POST["location"]
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            print(data)
            # Extract sunrise and sunset timestamps and convert them
            sunrise_timestamp = data['sys']['sunrise']
            sunset_timestamp = data['sys']['sunset']
            sunrise = datetime.fromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            sunset = datetime.fromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            # Add the formatted timestamps to the context
            
            return render(request,'home/dashboard.html',{'sunrise': sunrise,
                'sunset': sunset,"data":data})
        else:
            return render(request,'home/dashboard.html',{"error":"No Such City Found"})
    else:
        return render(request,'home/dashboard.html')

def about_view(request):
    return render(request,'home/about.html')

def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_view')

    # Get the 'next' parameter from the URL if it exists
    next_url = request.GET.get('next', 'dashboard_view')  # Default to 'home_view' if 'next' is not provided

    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            user = None

        if user is None:
            error = "User Not Found. Please Sign Up First."
            return render(request, 'registration/login.html', {'error': error})

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the next URL if valid, otherwise go to the home page
            if url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('dashboard_view')
        else:
            error = "Incorrect Username/Email or Password."
            return render(request, 'registration/login.html', {'error': error})

    return render(request, 'registration/login.html', {'next': next_url})



def signup_view(request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('signup_view')

    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('dashboard_view')
        else:
            # Collect all form errors
            errors = form.errors
            return render(request, 'registration/signup.html', {'form': form, 'errors': errors})
    else:
        form = UserSignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    
@login_required(login_url='/login?next=/predict')
def predict_view(request):
    return render(request, 'home/predict.html')


def logout_view(request):
    logout(request)
    return redirect('home_view')

@login_required
def profile_view(request):
    return render(request,'registration/profile.html')

@login_required
def profile_edit_view(request):
    user = request.user

    # Try to get the Notify object for the user, if it exists
    try:
        notify = Notify.objects.get(user=user)
    except Notify.DoesNotExist:
        notify = None

    if request.method == "POST":
        # Initialize both forms with POST data
        profile_form = UserProfileEditForm(request.POST, instance=user)
        notify_form = NotifyForm(request.POST)

        if profile_form.is_valid() and notify_form.is_valid():
            # Save the user profile form
            profile_form.save()

            # Handle the notify form logic based on the conditions
            get_notifications = request.POST.get('get_notifications', False)
            preferred_location = notify_form.cleaned_data['preferred_location']

            # Apply update conditions
            if get_notifications == 'on' and preferred_location:
                if notify is None:
                    notify = Notify(user=user, preferred_location=preferred_location)
                else:
                    notify.preferred_location = preferred_location
                notify.save()

            elif get_notifications != 'on' and not preferred_location:
                if notify:
                    notify.delete()

            return redirect('profile_view')  # Redirect after successful update
        else:
            # print(profile_form.errors, notify_form.errors)
            # Pass errors back to the template
            return render(request, 'registration/profile_edit.html', {
                'profile_form': profile_form,
                'notify_form': notify_form,
                'errors': profile_form.errors | notify_form.errors
            })

    else:
        # Initialize forms with existing user data and Notify data if available
        profile_form = UserProfileEditForm(instance=user)
        initial_data = {
            'preferred_location': notify.preferred_location if notify else '',
            'get_notifications': bool(notify)
        }
        notify_form = NotifyForm(initial=initial_data)

    return render(request, 'registration/profile_edit.html', {
        'profile_form': profile_form,
        'notify_form': notify_form
    })

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save feedback form data
            feedback = form.save(user=request.user)  # Save with optional user
           
            return redirect('dashboard_view')  # Redirect to homepage after submitting
    else:
        form = FeedbackForm()
    
    return render(request, 'home/feedback.html', {'form': form})