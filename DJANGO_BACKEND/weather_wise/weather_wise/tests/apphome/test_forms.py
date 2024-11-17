import pytest
from django.contrib.auth.models import User
from app_home.forms import UserSignUpForm, UserProfileEditForm, NotifyForm, FeedbackForm
from django.core.exceptions import ValidationError
from app_home.models import Notify, Feedback

# to test if user is able to signup
@pytest.mark.django_db
def test_user_signup_form_valid():
    data = {
        'username': 'Sumitg',
        'email': 'sumit123@example.com',
        'first_name': 'Sumit',
        'last_name': 'Vish',
        'password1': 'madhav123',
        'password2': 'madhav123',
    }
    form = UserSignUpForm(data)
    print(form.errors)
    assert form.is_valid()  # to check if form is valid

@pytest.mark.django_db
def test_user_signup_form_invalid_username():
    # to test a user for duplicate username validation
    User.objects.create_user(username='Sumitg', email='sumit2@example.com', password='shravan12345')
    
    data = {
        'username': 'Sumitg', 
        'email': 'sumit2@example.com',
        'first_name': 'New',
        'last_name': 'Sumit',
        'password1': 'shravan12345',
        'password2': 'shravan12345',
    }
    form = UserSignUpForm(data)
    print(form.errors)
    assert not form.is_valid()  
    assert 'This username is already taken. Please choose another one.' in form.errors['username']


@pytest.mark.django_db
def test_user_signup_form_invalid_email():
    # Create a user for email validation
    User.objects.create_user(username='testuser2', email='testuser@example.com', password='password123')
    
    data = {
        'username': 'newuser',
        'email': 'testuser@example.com',  # Duplicate email
        'first_name': 'New',
        'last_name': 'User',
        'password1': 'newpassword123',
        'password2': 'newpassword123',
    }
    form = UserSignUpForm(data)
    assert not form.is_valid()  # Form should not be valid
    assert 'This email address is already registered. Please log in instead.' in form.errors['email']

#to test update user profile
@pytest.mark.django_db
def test_user_profile_edit_form_invalid():
    user = User.objects.create_user(username='Sumit3', email='sumit345@example.com', password='shravan333')
    data = {
        'username': 'Sumit3',
        'email': 'sumit345example.com',   # intentionally entered invalid email format
        'first_name': 'Test',
        'last_name': 'ing',
    }
    form = UserProfileEditForm(data, instance=user)
    print(form.errors)
    assert not form.is_valid()  

#to test update user profile
@pytest.mark.django_db
def test_user_profile_edit_form_valid():
    user = User.objects.create_user(username='Sumit3', email='sumit345@example.com', password='shravan333')
    data = {
        'username': 'Sumit3',
        'email': 'sumit345@example.com',   #  entered valid email format
        'first_name': 'Test',
        'last_name': 'ing',
    }
    form = UserProfileEditForm(data, instance=user)
    print(form.errors)
    assert form.is_valid()  

# to test notify form 
@pytest.mark.django_db
def test_notify_form_valid():
    data = {
        'get_notifications': True,
        'preferred_location': 'New York',
    }
    form = NotifyForm(data)
    assert form.is_valid()  

@pytest.mark.django_db
def test_notify_form_invalid_notifications():
    data = {
        'get_notifications': False,         # but receive notification field is False
        'preferred_location': 'Ahmedabad',  #non empty field
    }
    form = NotifyForm(data)
    assert not form.is_valid()  # Form should not be valid
    assert 'You need to enable notifications to have a preferred location.' in form.errors['__all__']

# to test feedback form functionality
@pytest.mark.django_db
def test_feedback_form_valid():
    data = {
        'predictions_accuracy': 'accurate',
        'app_usability': 'easy',
        'user_interface': 'intuitive',
        'helpful_info': 'helpful',
        'app_recommend': 'yes',
    }
    form = FeedbackForm(data)
    assert form.is_valid()  

# to test if the form is saved successfully
@pytest.mark.django_db
def test_feedback_form_save():
    data = {
        'predictions_accuracy': 'accurate',
        'app_usability': 'easy',
        'user_interface': 'intuitive',
        'helpful_info': 'helpful',
        'app_recommend': 'yes',
    }
    form = FeedbackForm(data)
    assert form.is_valid()  # to test the form is valid before saving
    user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
    feedback = form.save(user=user)

    # to test if the feedback object was created and saved properly
    assert Feedback.objects.count() == 1
    assert feedback.user == user
    assert feedback.predictions_accuracy == 'accurate'
    assert feedback.app_usability == 'easy'
    assert feedback.user_interface == 'intuitive'
    assert feedback.helpful_info == 'helpful'
    assert feedback.app_recommend == 'yes'
