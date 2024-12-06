from django.shortcuts import render,redirect
from app_home.forms import UserSignUpForm,UserProfileEditForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Notify, Recent_loc,Fav_loc
from .forms import NotifyForm,FeedbackForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
from django.utils.http import url_has_allowed_host_and_scheme
import requests
from datetime import datetime
import os
import pickle
from .pipeline import format_prediction_output  # relative import if within the same app
from .pipeline import WeatherPipeline
from django.conf import settings
from django.http import JsonResponse
from .utils import send_notification_email
import random
import logging

API_KEY_1 = settings.WEATHER_API_KEY_1


logger = logging.getLogger('custom_logger')

def get_weather_data(city):
    """ 
    Fetch weather data for a given city and return sunrise and sunset times.
    Parameters:
        city (str): The city name.
        api_key (str): The API key for OpenWeather API.
    Returns:
        dict: A dictionary containing the city name, sunrise, and sunset times in the specified format.
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_1}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        sunrise_timestamp = data['sys']['sunrise']
        sunset_timestamp = data['sys']['sunset']
        
        data['sys']['sunrise'] = datetime.fromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        data['sys']['sunset'] = datetime.fromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'city': city,
            'data': data,
        }
    else:
        return {'error': f"Failed to get data for {city}"}

def home_view(request):
    if request.method == "POST":
        city = request.POST["location"]
        weather_info = get_weather_data(city)

        if 'error' in weather_info:
            return render(request, 'home/home.html', {"error": weather_info['error']})
        else:
            return render(request, 'home/home.html', {'data': weather_info['data']})
        
    else:
        city1 = 'Delhi'
        weather_info1 = get_weather_data(city1)
        city2 = 'Mumbai'
        weather_info2 = get_weather_data(city2)
        city3 = 'Hyderabad'
        weather_info3 = get_weather_data(city3)
        return render(request, 'home/home.html', {
            'data_Delhi': weather_info1['data'],
            'data_Mumbai': weather_info2['data'],
            'data_Hyderabad': weather_info3['data'],
        })
    
@login_required    
def dashboard_view(request):
    user = request.user

    if request.method == "POST":
        print(request.POST)
        if "fav_location_save" in request.POST:
            city = request.POST.get("fav_location_save")
            #print(f"Save request for {request.POST.get("fav_location_save")}")
            checkExist = Fav_loc.objects.filter(user=user, favourite_location=city).first()
            # save only if already not saved
            if not checkExist:
                Fav_loc.objects.create(user=user, favourite_location=request.POST.get("fav_location_save"))
            favlocs_data = []
            favlocs = Fav_loc.objects.filter(user=user)  # Retrieve all favorite locations for the user
            for loc in favlocs :
                weather_info = get_weather_data(loc.favourite_location)
                # print(weather_info['data'])
                favlocs_data.append(weather_info['data'])
            return render(request, 'home/dashboard.html', { 'fav_locs_data': favlocs_data })
        if "fav_location_delete" in request.POST:
            #print(f"Delete request for {request.POST.get("fav_location_delete")}")
            # Delete the favorite location from the database
            Fav_loc.objects.filter(user=user, favourite_location=request.POST.get("fav_location_delete")).delete()
            favlocs_data = []
            favlocs = Fav_loc.objects.filter(user=user)  # Retrieve updated favorite locations for the user
            for loc in favlocs :
                weather_info = get_weather_data(loc.favourite_location)
                # print(weather_info['data'])
                favlocs_data.append(weather_info['data'])
            return render(request, 'home/dashboard.html', { 'fav_locs_data': favlocs_data })
        if "location" in request.POST:
            #print(f"Search request for {request.POST.get("location")}")
            city = request.POST["location"]
            weather_info = get_weather_data(city)

            if 'error' in weather_info:
                return render(request, 'home/home.html', {"error": weather_info['error']})
            else:
                return render(request, 'home/dashboard.html', {
                    'data': weather_info['data'],
                })
    else:
        favlocs_data = []
        favlocs = Fav_loc.objects.filter(user=user)  # Retrieve all favorite locations for the user
        for loc in favlocs :
                weather_info = get_weather_data(loc.favourite_location)
                # print(weather_info['data'])
                favlocs_data.append(weather_info['data'])
        return render(request, 'home/dashboard.html', { 'fav_locs_data': favlocs_data })

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
        notify_form = NotifyForm(request.POST)

        if form.is_valid() and notify_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Handle Notify object logic
            try:
                notify = Notify.objects.get(user=user)
            except Notify.DoesNotExist:
                notify = None

            get_notifications = request.POST.get('get_notifications', False)
            preferred_location = notify_form.cleaned_data['preferred_location']
            get_notifications = True if get_notifications == 'on' else False

            if get_notifications and preferred_location:
                if notify is None:
                    notify = Notify(user=user, preferred_location=preferred_location, get_notifications=get_notifications)
                else:
                    notify.preferred_location = preferred_location
                notify.save()

            otp_ = random.randint(1000, 9999)
            subject = "WeatherWise Account Verification"
            message = f"Dear user, your One Time Verification password is: {otp_}"
            recipient_list = [user.email]  # Replace with actual user emails
            email_sent = send_notification_email(subject, message, recipient_list)

            # Store user ID and OTP in session for OTP verification
            request.session['user_id'] = user.id
            request.session['otp'] = otp_

            if email_sent:
                return redirect('otp_verify')
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to send email.'})

        else:
            return render(request, 'registration/signup.html', {
                'form': form,
                'notify_form': notify_form,
                'errors': form.errors | notify_form.errors
            })
    else:
        form = UserSignUpForm()
        notify_form = NotifyForm()
        return render(request, 'registration/signup.html', {
            'form': form,
            'notify_form': notify_form
        })


@login_required
def logout_view(request):
    logout(request)
    # Clear theme preference
    if 'is_dark_theme' in request.session:
        del request.session['is_dark_theme']
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

            # Convert 'on' to True, otherwise False
            get_notifications = True if get_notifications == 'on' else False

            # Apply update conditions
            if get_notifications and preferred_location:
                if notify is None:
                    notify = Notify(user=user, preferred_location=preferred_location, get_notifications=get_notifications)
                else:
                    notify.preferred_location = preferred_location
                notify.save()

            elif not get_notifications:
                if notify:
                    notify.delete()

            return redirect('profile_view')  # Redirect after successful update
        else:
            # Pass errors back to the template
            return render(request, 'registration/profile_edit.html', {
                'profile_form': profile_form,
                'notify_form': notify_form,
                'notify': notify,
                'errors': profile_form.errors | notify_form.errors  # Combine errors from both forms
            })

    else:
        profile_form = UserProfileEditForm(instance=user)
        notify_form = NotifyForm(instance=notify)

        return render(request, 'registration/profile_edit.html', {
            'profile_form': profile_form,
            'notify_form': notify_form,
            'notify': notify,
            'errors': {}
        })

@login_required(login_url='/login?next=/predict')
def predict_view(request):
    YOUR_ACCESS_KEY = '6d01b78a047e5aa7f1b705ad7cdbfde7'
    user = request.user
    if request.method == "POST":
        city = request.POST["location"]
        url = "http://api.weatherstack.com/current"
        querystring = {"access_key": YOUR_ACCESS_KEY, "query": city}
        response = requests.get(url, params=querystring)
        data = response.json()
        # Extract weather features
        weather_info = {
            'temperature': float(data['current']['temperature']),
            'humidity': float(data['current']['humidity']),
            'wind_speed': float(data['current']['wind_speed']),
            'precipitation': float(data['current']['precip']),
        }
        #print(weather_info)
        # Use the extracted data for prediction
        input_data = [weather_info['temperature'], weather_info['humidity'],
                      weather_info['wind_speed'], weather_info['precipitation']]
        predictions = None  # Initialize predictions to handle errors
        try:
            # Load the prediction pipeline
            pipeline = WeatherPipeline()
            predictions = pipeline.predict(input_data)
            logger.debug("Pipeline initialized successfully.")
            logger.debug(f"Input data: {input_data}")
            logger.debug(f"Predictions: {predictions}")
        except Exception as e:
            # formatted_predictions = f"Error during prediction: {str(e)}"
            #print(f"Error during prediction: {str(e)}")
            # Log the error
            logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        # Save recent location
        Recent_loc.objects.create(user=user, recent_location=city)
        return render(request, 'home/predict.html', {
            'city': city.upper(),
            'predictions': predictions
        })
    else:
        # Fetch top 3 recent locations for the user
        recentLocs = (
            Recent_loc.objects.filter(user=user)
            .values('recent_location')
            .annotate(search_count=Count('recent_location'))
            .order_by('-search_count')[:3]
        )
        return render(request, 'home/predict.html', {'recentLocs': recentLocs})
    
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


def send_weather_alert(request):
    if request.method == 'POST':
        otp = random.randint(1000, 9999)
        # Example data
        subject = "WeatherWise Account Verification"
        message = f"Dear user, your One Time Verification password is: {otp}"
        recipient_list = ['202201333@daiict.ac.in']  # Replace with actual user emails

        email_sent = send_notification_email(subject, message, recipient_list)

        if email_sent:
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to send email.'})

    return render(request, 'home/email_service.html')

def otp_verify(request):
    if request.method == 'POST':
        otp_ = request.session.get('otp')  # Get generated OTP
        otp = request.POST.get('otp')  # Get user-entered OTP
        user_id = request.session.get('user_id')  # Get user ID from session

        if not otp_ or not user_id:
            return redirect('signup_view')  # Redirect if session data is missing

        if 'otp_attempts' not in request.session:
            request.session['otp_attempts'] = 0

        # Retrieve attempt count from session
        otp_attempts = request.session['otp_attempts']

        if str(otp_) == str(otp):
            # OTP is correct, log in the user
            try:
                user = User.objects.get(id=user_id)
                login(request, user)

                # Clear session data after successful verification
                for key in ['user_id', 'otp', 'otp_attempts']:
                    if key in request.session:
                        del request.session[key]

                return redirect('dashboard_view')
            except User.DoesNotExist:
                return redirect('signup_view')  # Handle case where user doesn't exist
        else:
            # Increment and save the number of attempts
            otp_attempts += 1
            request.session['otp_attempts'] = otp_attempts

            # Check if attempts exceed limit
            if otp_attempts >= 3:
                # Delete the user from the database
                try:
                    user = User.objects.get(id=user_id)
                    user.delete()
                except User.DoesNotExist:
                    pass  # User might already be deleted
                
                # Clear session data
                for key in ['user_id', 'otp', 'otp_attempts']:
                    if key in request.session:
                        del request.session[key]

                return render(request, 'registration/signup.html', {
                    'error': 'Too many incorrect attempts. Please sign up again.'
                })

            return render(request, 'home/otp_verify.html', {
                'error': f'Invalid OTP. {3 - otp_attempts} attempts remaining.'
            })

    return render(request, 'home/otp_verify.html')