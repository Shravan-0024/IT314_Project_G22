from django.shortcuts import render,redirect
from app_home.forms import UserSignUpForm
from django.contrib.auth import login,logout,authenticate

def home_view(request):
    return render(request,'home/home.html')

def about_view(request):
    return render(request,'home/about.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home_view')
        else:
            return render(request,'registration/login.html')
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