import pytest
from django.contrib.auth.models import User
from app_home.models import Feedback, Notify, Fav_loc
from django.core.exceptions import ValidationError

print("Sumit testing: Feedback, Notify and Favorite Locations Models")
@pytest.fixture
def user():
    # creating a test user
    return User.objects.create_user(username='Sumit', password='sumit_is_testing')


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
    # to test that a Feedback instance is created successfully
    assert feedback.user.username == 'Sumit'
    assert feedback.predictions_accuracy == 'accurate'
    assert feedback.app_usability == 'easy'
    assert feedback.user_interface == 'intuitive'
    assert feedback.helpful_info == 'helpful'
    assert feedback.app_recommend == 'yes'


@pytest.mark.django_db 
def test_null_fields(user):
    # to test that empty fields are not saved in the database
    feedback = Feedback.objects.create(user=user, predictions_accuracy='accurate')
    assert feedback.app_usability is None
    assert feedback.user_interface is None
    assert feedback.helpful_info is None
    assert feedback.app_recommend is None


@pytest.mark.django_db  
def test_feedback_str(feedback):
    # to test the __str__ method for the Feedback model
    assert str(feedback) == f"Feedback from {feedback.user.username}"

    # to test that feedback model has no associated user
    feedback_anonymous = Feedback.objects.create(user=None, predictions_accuracy='accurate')
    assert str(feedback_anonymous) == "Anonymous Feedback"


@pytest.mark.django_db  
def test_notify_creation(notify):
    # to test that a Notify instance is created successfully
    assert notify.user.username == 'Sumit'
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
    # to test for a user to have only one Notify instance
    Notify.objects.create(user=user, preferred_location='Ahmedabad')
    assert Notify.objects.count() == 1  # Only one Notify instance should exist


@pytest.mark.django_db
def test_notify_str(notify):
    # to test the __str__ method for the Notify model
    assert str(notify) == f"Notify preferences for {notify.user.username}"



@pytest.mark.django_db 
@pytest.mark.parametrize("invalid_value", ['invalid_choice', 'unknown', 'untrusted'])
def test_feedback_choices(feedback, invalid_value):
    # to test that 'app_recommend' field has valid choices
    valid_choices = ['yes', 'no', 'maybe']
    
    feedback.app_recommend = invalid_value
    with pytest.raises(ValidationError):
        feedback.full_clean()  # Should raise a validation error for invalid choices


@pytest.mark.django_db  
def test_notify_user_preference(user):
    # tp test that Notify instance follows the user preference location
    notify = Notify.objects.create(user=user, preferred_location='Bangalore')
    assert notify.preferred_location == 'Bangalore'

    #  to test updating the preferred location
    notify.preferred_location = 'Delhi'
    notify.save()
    assert notify.preferred_location == 'Delhi'


# Below are the testcases for Favorite Locations Model
@pytest.fixture
def user():
    # Create a test user
    return User.objects.create_user(username="Sumit", email="Sumit@example.com", password="sumit_is_testing")


@pytest.mark.django_db
def test_valid_fav_loc_creation(user):
    # to test the creation of a valid Fav_loc instance
    fav_loc = Fav_loc.objects.create(user=user, favourite_location="Mumbai")
    assert Fav_loc.objects.count() == 1
    assert fav_loc.favourite_location == "Mumbai"
    assert fav_loc.user == user

@pytest.mark.xfail(reason="creating fav_loc with empty favourite_location is expected to fail!")
@pytest.mark.django_db
def test_invalid_empty_fav_loc(user):
    # to test that creating a fav_loc instance with an empty string fails
    fav_loc = Fav_loc(user=user, favourite_location="")
    if fav_loc.favourite_location == "": #I intentionally entered empty field!
        raise ValidationError("Favourite location cannot be empty.")

@pytest.mark.xfail(reason="entering favorite location string with more than 100 chars is expected to fail!")
@pytest.mark.django_db
def test_fav_loc_max_length(user):
    long_location = "Gandhinagar"*101  # I intentionally exceeded max_length of 100
    fav_loc = Fav_loc(user=user, favourite_location=long_location) 
    if len(long_location) > 100:
        raise ValidationError("Favourite location string cant exceed 100 chars!")


@pytest.mark.django_db
def test_valid_multiple_fav_locs(user):
    # to test that a user can have multiple favorite locations
    fav_loc1 = Fav_loc.objects.create(user=user, favourite_location="Shimla")
    fav_loc2 = Fav_loc.objects.create(user=user, favourite_location="Varanasi")
    
    assert Fav_loc.objects.count() == 2
    assert fav_loc1.favourite_location == "Shimla"
    assert fav_loc2.favourite_location == "Varanasi"
    assert fav_loc1.user == user
    assert fav_loc2.user == user


@pytest.mark.django_db
def test_fav_loc_str(user):
    # to test the __str__ method of Fav_loc model
    fav_loc = Fav_loc.objects.create(user=user, favourite_location="Lucknow")
    assert str(fav_loc) == f"Favourite location for {user.username}"