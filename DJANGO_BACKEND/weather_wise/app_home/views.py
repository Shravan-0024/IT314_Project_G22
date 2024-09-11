from django.shortcuts import render

def home_view(request):
    return render(request,'home/home.html')

def about_view(request):
    return render(request,'home/about.html')

def login_view(request):
    return render(request,'registration/login.html')

def signup_view(request):
    return render(request,'registration/signup.html')

def predict_view(request):
    return render(request,'home/predict.html')