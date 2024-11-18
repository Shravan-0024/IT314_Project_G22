import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
@pytest.mark.parametrize("path,view_name,requires_auth,expected_status", [
    ('/', 'home_view', False, 200),
    ('/about/', 'about_view', False, 200),
    ('/login/', 'login_view', False, 200),
    ('/dashboard/', 'dashboard_view', True, 200), # we need user to be logged in for this page
    ('/logout/', 'logout_view', True, 302),  # here expected_status=302 -> because of redirect to home page after logout
    ('/signup/', 'signup_view', False, 200),
    ('/predict/', 'predict_view', True, 200),
    ('/profile/', 'profile_view', True, 200),
    ('/profile/edit/', 'profile_edit_view', True, 200),
    ('/feedback/', 'feedback_view', True, 200), # similar here, we need user to be logged in for this page
    ('/switch-theme/', 'change-theme', False, 302), 
])
def test_urls(client, django_user_model, path, view_name, requires_auth, expected_status):
    if requires_auth:
        # first creating and logging in a test user
        user = django_user_model.objects.create_user(username='Sumit', password='Vishwakarma')
        client.login(username='Sumit', password='Vishwakarma')

    response = client.get(path)  # this sends a get request to the path we are testing
    
    assert response.status_code == expected_status  # this assert checks the expected status (as mentioned in the parametrize arguments)
                                                    # 200 meaning OK and 302 meaning redirect 