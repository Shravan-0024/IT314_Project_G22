from django.urls import path
from app_home import views
urlpatterns = [
    path('',views.home_view,name="home_view"),
    path('about/',views.about_view,name="about_view"),
]
