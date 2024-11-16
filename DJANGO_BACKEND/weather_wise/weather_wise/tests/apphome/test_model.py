import pytest
from django.contrib.auth.models import User
from app_home.models import Feedback, Notify
from django.core.exceptions import ValidationError


@pytest.fixture
def user():
    # creating a test user
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def feedback(user):
    # creating a feedback instance
    return Feedback.objects.create(
        user=user,
        predictions_accuracy='accurate',
        app_usability='easy',
        user_interface='intuitive',
        helpful_info='helpful',
        app_recommend='yes'
    )


@pytest.fixture
def notify(user):
    # creating a notify instance
    return Notify.objects.create(
        user=user,
        preferred_location='Mumbai'
    )


@pytest.mark.django_db 
def test_feedback_creation(feedback):
    # Test that a Feedback instance is created successfully
    assert feedback.user.username == 'testuser'
    assert feedback.predictions_accuracy == 'accurate'
    assert feedback.app_usability == 'easy'
    assert feedback.user_interface == 'intuitive'
    assert feedback.helpful_info == 'helpful'
    assert feedback.app_recommend == 'yes'


@pytest.mark.django_db 
def test_null_fields(user):
    # Test that empty fields are not saved in the database
    feedback = Feedback.objects.create(user=user, predictions_accuracy='accurate')
    assert feedback.app_usability is None
    assert feedback.user_interface is None
    assert feedback.helpful_info is None
    assert feedback.app_recommend is None


@pytest.mark.django_db  
def test_feedback_str(feedback):
    # Test the __str__ method for the Feedback model
    assert str(feedback) == f"Feedback from {feedback.user.username}"

    # Case 2: Feedback has no associated user
    feedback_anonymous = Feedback.objects.create(user=None, predictions_accuracy='accurate')
    assert str(feedback_anonymous) == "Anonymous Feedback"


@pytest.mark.django_db  
def test_notify_creation(notify):
    # Test that a Notify instance is created successfully
    assert notify.user.username == 'testuser'
    assert notify.preferred_location == 'Mumbai'


@pytest.mark.django_db 
@pytest.mark.parametrize("location, expected", [
    ('mumbai', 'mumbai'),
    ('A' * 256, None),  # This should trigger validation error if the length exceeds max_length
])
def test_preferred_location_max_length(user, location, expected):
    # Test that the preferred_location field enforces max_length
    notify = Notify(user=user, preferred_location=location)
    if expected is None:
        with pytest.raises(ValidationError):
            notify.full_clean()  # This should raise a validation error if max_location not enforced
    else:
        try:
            notify.full_clean()  # Full validation
            notify.save()  
        except ValidationError as e:
            pytest.fail(f"Validation failed: {e}")
        assert notify.preferred_location == expected


@pytest.mark.django_db  
@pytest.mark.xfail(reason="Expected to fail if user has more than one Notify instance")
def test_unique_user(user, notify):
    # Testcase for a user to have only one Notify instance
    Notify.objects.create(user=user, preferred_location='Ahmedabad')
    assert Notify.objects.count() == 1  # Only one Notify instance should exist


@pytest.mark.django_db
def test_notify_str(notify):
    # Testcase for testing the __str__ method for the Notify model
    assert str(notify) == f"Notify preferences for {notify.user.username}"



@pytest.mark.django_db 
@pytest.mark.parametrize("invalid_value", ['invalid_choice', 'unknown', 'untrusted'])
def test_feedback_app_recommend_choices(feedback, invalid_value):
    # Tests that 'app_recommend' field has valid choices
    valid_choices = ['yes', 'no', 'maybe']
    
    feedback.app_recommend = invalid_value
    with pytest.raises(ValidationError):
        feedback.full_clean()  # Should raise a validation error for invalid choices


@pytest.mark.django_db  
def test_notify_user_preference(user):
    # Test that Notify instance respects the user preference location
    notify = Notify.objects.create(user=user, preferred_location='Bangalore')
    assert notify.preferred_location == 'Bangalore'

    # Test updating the preferred location
    notify.preferred_location = 'Delhi'
    notify.save()
    assert notify.preferred_location == 'Delhi'
