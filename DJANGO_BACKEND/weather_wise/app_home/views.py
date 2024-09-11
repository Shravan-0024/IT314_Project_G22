from django.shortcuts import render

def home_view(request):
    return render(request,'home/home.html')

def about_view(request):
    return render(request,'home/about.html')