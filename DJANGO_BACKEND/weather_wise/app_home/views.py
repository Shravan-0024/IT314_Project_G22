from django.shortcuts import render,redirect
from app_home.forms import UserSignUpForm
from django.contrib.auth import login,logout

def home_view(request):
    return render(request,'home/home.html')

def about_view(request):
    return render(request,'home/about.html')

def login_view(request):
    return render(request,'registration/login.html')

def signup_view(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home_view')
    else:
        form = UserSignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

def predict_view(request):
    return render(request,'home/predict.html')

def logout_view(request):
    logout(request)
    return redirect('home_view')