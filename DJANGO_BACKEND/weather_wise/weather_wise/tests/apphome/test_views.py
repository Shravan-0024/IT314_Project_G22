import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from app_home.models import Fav_loc, Notify, Recent_loc
from app_home.models import Feedback


# this is to test the get request of home view
@pytest.mark.django_db
def test_home_view_get(client):
    
    #this test checks the return of default weather data for predefined cities (as metioned in the views.py file)
    
    url = reverse('home_view')
    response = client.get(url)
    assert response.status_code == 200
    assert 'data_Delhi' in response.context    #this verifies that the home_view view passes the weather data to the template.
    assert 'data_Mumbai' in response.context
    assert 'data_Hyderabad' in response.context

@pytest.mark.django_db
def test_home_view_post(client):
    # to test that home view ressponds to POST request
    url = reverse('home_view')  
    response = client.post(url, {'location': 'Gandhinagar'})  # entering an valid city name
    assert response.status_code == 200

    # Check that there is no error is in the response
    assert 'data' in response.context
    assert 'error' not in response.context
 
@pytest.mark.django_db
def test_home_view_post_with_error(client):
    url = reverse('home_view')  
    response = client.post(url, {'location': 'InvalidCity'})  # entering an invalid city name
    assert response.status_code == 200

    # Check that the error message is in the context
    assert 'error' in response.context
    assert "Some Error Occured for 'InvalidCity'" in response.context['error'] # as mentioned in views.py file

@pytest.mark.django_db
def test_post_city(client):
    
    # this is to test that the homeview correctly handels a POST request for city
    url = reverse('home_view')
    response = client.post(url, {'location': 'Gandhinagar'})  # simulating a post request
    assert response.status_code == 200
    assert 'data' in response.context  # checks if the data is passed form the template successfully


@pytest.mark.django_db
def test_dashboard_view_authenticated_user(client, django_user_model):
    
    #this is to check the dashboard view for a logged in user
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')
    url = reverse('dashboard_view')
    response = client.get(url)
    assert response.status_code == 200  # confirms that there are no redirects
    assert 'fav_locs_data' in response.context  # checks if the fav_locs data is passed successfully


@pytest.mark.django_db
def test_dashboard_add_favorite(client, django_user_model):
    
    # this is to check logged in user adding a favorite location in the dashboard view
    user = django_user_model.objects.create_user(username='Shravan', password='Kakadiya')
    client.login(username='Shravan', password='Kakadiya')

    url = reverse('dashboard_view')
    response = client.post(url, {'fav_location_save': 'Ahmedabad'})  # creating an instance of fav_location
    assert response.status_code == 200  # checks if there is no redirect to other page
    assert Fav_loc.objects.filter(user=user, favourite_location='Ahmedabad').exists() # to check that the fav loc is passed successfully

@pytest.mark.django_db
def test_dashboard_no_favorites(client, django_user_model):
    # to test that the dashboard renders correctly for a user with no favorite locations.
    user = django_user_model.objects.create_user(username='NoFavsUser', password='password')
    client.login(username='NoFavsUser', password='password')
    
    url = reverse('dashboard_view')
    response = client.get(url)

    assert response.status_code == 200
    assert 'fav_locs_data' in response.context 
    assert len(response.context['fav_locs_data']) == 0  # Ensures no fav location data is present

def test_dashboard_delete_favorite(client, django_user_model):
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')
    
    # Add a favorite location to the database first
    Fav_loc.objects.create(user=user, favourite_location='Ahmedabad')
    
    # Delete the favorite location
    url = reverse('dashboard_view')
    response = client.post(url, {'fav_location_delete': 'Ahmedabad'})  # Deleting Ahmedabad
    assert response.status_code == 200  
    assert not Fav_loc.objects.filter(user=user, favourite_location='Ahmedabad').exists() 
    assert 'fav_locs_data' in response.context  
    assert len(response.context['fav_locs_data']) == 0  

def test_dashboard_search_location(client, django_user_model):
    #creating an instance
    user = django_user_model.objects.create_user(username='Shravan', password='Kakadiya')
    client.login(username='Shravan', password='Kakadiya')

    # Simulate searching for a location
    url = reverse('dashboard_view')
    response = client.post(url, {'location': 'Anand'}) 
    
    assert response.status_code == 200
    assert 'data' in response.context  
    assert response.context['data']['name'] == 'Anand'

@pytest.mark.django_db
def test_dashboard_search_invalid_location(client, django_user_model):
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')

    # Simulate an invalid location search
    url = reverse('dashboard_view')
    response = client.post(url, {'location': 'InvalidCity'})  # An invalid city name
    print(response.context)
    assert response.status_code == 200
    assert 'error' in response.context  
    assert "Some error occurred for 'InvalidCity'" in response.context['error']  # Checking the error message content

@pytest.mark.django_db
def test_dashboard_multiple_favorites(client, django_user_model):
    # to test multiple favorite locations
    user = django_user_model.objects.create_user(username='Shravan', password='Kakadiya')
    client.login(username='Shravan', password='Kakadiya')
    
    # Adding 2 favorite locations
    Fav_loc.objects.create(user=user, favourite_location='Ahmedabad')
    Fav_loc.objects.create(user=user, favourite_location='Anand')
    
    url = reverse('dashboard_view')
    response = client.get(url)

    assert response.status_code == 200
    
    assert 'fav_locs_data' in response.context
    assert len(response.context['fav_locs_data']) == 2  # Two locations should be passed


API_KEY = "3fd909629968761c4f36f936ba57ef90" 

@pytest.mark.django_db
def test_dashboard_view_with_fav_locations(client, django_user_model):
    # to test a dashboard with fav_locations
    user = django_user_model.objects.create_user(username='Sumit', password='password123')
    client.login(username='Sumit', password='password123')
    Fav_loc.objects.create(user=user, favourite_location='Ahmedabad')
    
    # Make a POST request to add a favorite location
    url = reverse('dashboard_view')
    response = client.post(url, {'fav_location_save': 'Ahmedabad'})  #saving location
    assert response.status_code == 200
    assert 'fav_locs_data' in response.context

    # Verify that the data returned from the OpenWeatherMap API contains the expected values
    fav_locs_data = response.context['fav_locs_data']
    assert len(fav_locs_data) == 1  # We only added one location
    assert fav_locs_data[0]['name'] == 'Ahmedabad'
    assert 'main' in fav_locs_data[0]  # Check if the main data (like temperature) is present

@pytest.mark.django_db
def test_login_view_get(client):
    # to test the login view with get request
    url = reverse('login_view')
    response = client.get(url)
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_login_view_logout_redirect(client, django_user_model):
    # to test a user logout 
    user = django_user_model.objects.create_user(username='Sumit', password='password')
    client.login(username='Sumit', password='password')  # Log the user in
    url = reverse('login_view')
    response = client.get(url)

    # Verify that the user is logged out and redirected to the login page
    assert response.status_code == 302 
    assert response.url == reverse('login_view')  # Verify the redirection is to the login page

    # Verify the user is logged out
    assert not hasattr(response, 'user') or not response.user.is_authenticated


@pytest.mark.django_db
def test_login_view_post(client, django_user_model):
    # to test the login view POST request for authenticated user
    user = django_user_model.objects.create_user(username='Sharvil', password='Oza')
    url = reverse('login_view')  # generates url for login
    response = client.post(url, {'username_or_email': 'Sharvil', 'password': 'Oza'})  # simulating a POST request
    assert response.status_code == 302  # checks redirect to dashboard

@pytest.mark.django_db
def test_login_view_post_invalid_user(client):
    # testing to send a POST request with a non-existent username or email
    url = reverse('login_view')
    response = client.post(url, {
        'username_or_email': 'nonexistentuser@example.com',  # Email doesn't exist
        'password': 'password'
    })
    assert response.status_code == 200
    # expects an error for user with no email
    assert 'error' in response.context 
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_signup_view_get(client):
   # to check that signup view responds correctly to a GET request.

    url = reverse('signup_view')
    response = client.get(url)      # GET request from signup view
    assert response.status_code == 200
    assert 'form' in response.context  # to confirm that the view passes a form object 

@pytest.mark.django_db
def test_signup_view_post_invalid(client):
    # to verify that the signup_view correctly handles a POST request with valid data.
    url = reverse('signup_view')  # to fetch the url for signup_view
    response = client.post(url, {     
        'username': 'SaurabhSir',
        'password1': 'IT314',
        'password2': 'wrongpassword'
    })
    # due to wrong password it will stay on the same page (signup)
    assert response.status_code==200
    assert not User.objects.filter(username='SaurabhSir').exists()  # to check if the new account is created or not
    assert 'form' in response.context  # Form should be passed back to the template
    assert response.context['form'].errors # check form for errors
    assert 'password2' in response.context['form'].errors

@pytest.mark.django_db
def test_predict_view_post(client, django_user_model):
    # to test the predict_view
    user = django_user_model.objects.create_user(username='Nisarg', password='Modi')
    client.login(username='Nisarg', password='Modi')
    # URL for the predict view
    url = reverse('predict_view')
    # Data to send in the POST request
    post_data = {
        'location': 'Bangalore'  
    }

    # Send the POST request
    response = client.post(url, post_data)

    # Verify the response status code
    assert response.status_code == 200

    # chacking that the Recent_loc instance was created
    assert Recent_loc.objects.filter(user=user, recent_location='Bangalore').exists()
    assert 'data' in response.context
    assert response.context['data'] == 1  

@pytest.mark.django_db
def test_profile_view_user(client, django_user_model):
    # to test profile view for a logged in user
    user = django_user_model.objects.create_user(username='Bhavya', password='Shah')
    client.login(username='Bhavya', password='Shah')
    url = reverse('profile_view')
    response = client.get(url)  # simulate get request
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_edit_view_post_update_notifications(client, django_user_model):
    # Create a user and log in
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')

    # Create Notify object for the user
    notify = Notify.objects.create(user=user, preferred_location="Hyderabad", get_notifications=True)

    # The URL for the profile edit page
    url = reverse('profile_edit_view')
    data = {
        'get_notifications': True,
        'preferred_location': 'Bangalore'
    }
   
    # Send the POST request with the data
    response = client.post(url, data)
    assert response.status_code == 200

    # Fetch the updated Notify object and check if the notification preferences were updated
    notify.refresh_from_db()
    assert notify.get_notifications is True
    assert not notify.preferred_location == 'Bangalore'


@pytest.mark.django_db
def test_profile_edit_view_post_delete_notifications(client, django_user_model):
    # Create a user and log in
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')

    # Create Notify object for the user with notifications turned off
    notify = Notify.objects.create(user=user, preferred_location="Hyderabad", get_notifications=False)

    # The URL for the profile edit page
    url = reverse('profile_edit_view')

    # Data to delete the user's notification preferences
    data = {
        'get_notifications': False,
        'preferred_location': ''
    }
    # Send the POST request with the data
    response = client.post(url, data)
    # Assert that the user is same page
    assert response.status_code == 200


@pytest.mark.django_db
def test_feedback_view_post(client, django_user_model):
    # to test a user's form submission
    user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
    client.login(username='Sumit', password='Vishwakarma')

    # the URL for the feedback page
    url = reverse('feedback_view')

    # initializing the feedback data to send in the POST request
    feedback_data = {
        'predictions_accuracy': 'accurate', 
        'app_usability': 'easy', 
        'user_interface': 'intuitive', 
        'helpful_info': 'helpful',
        'app_recommend': 'yes'  
    }

    # Send the POST request with the feedback data
    response = client.post(url, feedback_data)
    # Assert that the form is valid and the user is redirected to the dashboard page
    assert response.status_code == 302
    assert response.url == reverse('dashboard_view')  # Confirm that it redirects to the dashboard view

    # Verify that the feedback was saved in the database
    feedback = Feedback.objects.get(user=user)
    assert feedback.predictions_accuracy == 'accurate'
    assert feedback.app_usability == 'easy'
    assert feedback.user_interface == 'intuitive'
    assert feedback.helpful_info == 'helpful'
    assert feedback.app_recommend == 'yes'
    