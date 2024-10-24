from django.shortcuts import render,redirect
from app_home.forms import UserSignUpForm,UserProfileEditForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Notify
from .forms import NotifyForm
from django.contrib.auth.models import User
from django.db.models import Q

def home_view(request):
    return render(request,'home/home.html')

def about_view(request):
    return render(request,'home/about.html')

def login_view(request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('login_view')

    if request.method == "POST":
        # Get the entered username/email and password
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            user = None

        # If no user was found, return a 'User Not Found' error
        if user is None:
            error = "User Not Found. Please Sign Up First."
            return render(request, 'registration/login.html', {'error': error})

        # Authenticate using the username (if found) and password
        user = authenticate(request, username=user.username, password=password)

        # If authentication is successful, log the user in
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            # If authentication failed, show error message
            error = "Incorrect Username/Email or Password."
            return render(request, 'registration/login.html', {'error': error})

    # Render the login form if the request is not POST
    return render(request, 'registration/login.html')


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
            return redirect('home_view')
        else:
            # Collect all form errors
            errors = form.errors
            return render(request, 'registration/signup.html', {'form': form, 'errors': errors})
    else:
        form = UserSignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    
@login_required(login_url='/login')
def predict_view(request):
    return render(request,'home/predict.html')

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
