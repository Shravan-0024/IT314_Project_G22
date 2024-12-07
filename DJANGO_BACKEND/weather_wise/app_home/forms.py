from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Notify,Feedback
import requests
from django.conf import settings
import requests
import re


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The username must be at least 3 characters long.',
            'max_length': 'The username cannot exceed 30 characters.',
        }
    )

    email = forms.EmailField(
        min_length=5,
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The email must be at least 5 characters long.',
            'max_length': 'The email cannot exceed 254 characters.',
        }
    )

    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The first name must be at least 2 characters long.',
            'max_length': 'The first name cannot exceed 50 characters.',
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The last name must be at least 2 characters long.',
            'max_length': 'The last name cannot exceed 50 characters.',
        }
    )

    password1 = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The password must be at least 8 characters long.',
            'max_length': 'The password cannot exceed 128 characters.',
        }
    )

    password2 = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'}),
        error_messages={
            'min_length': 'The confirmation password must be at least 8 characters long.',
            'max_length': 'The confirmation password cannot exceed 128 characters.',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-yellow-400'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain letters (a-z, A-Z).")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should only contain letters (a-z, A-Z).")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered. Please log in instead.")
        try:
            email_key = settings.KICKBOX_API_KEY
            url = f"https://api.kickbox.com/v2/verify?email={email}&apikey={email_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get('result') not in ['deliverable', 'risky']:
                raise ValidationError("The provided email address is not valid or deliverable.")
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"An error occurred while validating the email\nPlease try later...")

        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        # Validate password length
        if len(password1) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password1):
            errors.append("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password1):
            errors.append("Password must contain at least one lowercase letter.")

        # Check for at least one digit
        if not re.search(r'[0-9]', password1):
            errors.append("Password must contain at least one digit.")

        # Check for at least one special character
        if not re.search(r'[@$!%*?&]', password1):
            errors.append("Password must contain at least one special character (@, $, !, %, *, ?, &).")

        # Raise a single ValidationError with all issues
        if errors:
            raise ValidationError(errors)

        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Ensure both password fields are filled
        if not password1:
            self.add_error('password1', "This field is required.")
        if not password2:
            self.add_error('password2', "This field is required.")

        # Ensure passwords match
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields must match.")

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Ensure passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields must match.")

        return cleaned_data

class UserProfileEditForm(forms.ModelForm):

    first_name = forms.CharField(
    min_length=2,
    max_length=50, 
    widget=forms.TextInput(attrs={'class': 'form-control'}))
    error_messages={
        'min_length': 'The first name must be at least 2 characters long.',
        'max_length': 'The first name cannot exceed 50 characters.',
    }

    last_name = forms.CharField(
    min_length=2,
    max_length=50, 
    widget=forms.TextInput(attrs={'class': 'form-control'}))
    error_messages={
        'min_length': 'The last name must be at least 2 characters long.',
        'max_length': 'The last name cannot exceed 50 characters.',
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        # Make username read-only since it's generally not editable
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].min_length = 3
        self.fields['username'].max_length = 30
        # Make email read-only since it's generally not editable
        self.flds['email'].widget.attrs['readonly'] = True
        self.fields['email'].min_length = 5
        self.fields['email'].max_length = 254

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email address is already registered with another account.")
        try:
            email_key = settings.KICKBOX_API_KEY
            url = f"https://api.kickbox.com/v2/verify?email={email}&apikey={email_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get('result') not in ['deliverable', 'risky']:
                # print("Invalid email")
                raise ValidationError("The provided email address is not valid or deliverable.")
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"An error occurred while validating the email\nPlease try later...")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should only contain letters (a-z, A-Z).")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should only contain letters (a-z, A-Z).")
        return last_name

class NotifyForm(forms.ModelForm):
    get_notifications = forms.BooleanField(required=False, label="Receive Weather Alerts!")
    preferred_location = forms.CharField(
    min_length=1,
    max_length=100,
    required=False, label="Preferred Location")
    error_messages={
        'min_length': 'The location must be at least 1 character long.',
        'max_length': 'The location cannot exceed 50 characters.',
    }

    class Meta:
        model = Notify
        fields = ['preferred_location']

    def clean(self):
        cleaned_data = super().clean()
        get_notifications = cleaned_data.get('get_notifications')
        preferred_location = cleaned_data.get('preferred_location')

        # Validation logic
        if get_notifications and not preferred_location:
            raise ValidationError("Enter a valid location if you want notifications.")

        return cleaned_data

class FeedbackForm(forms.Form):
    RECOMMEND_CHOICES = [
        ('yes', '👍 Yes, I would recommend this app'),
        ('no', '👎 No, I would not recommend it'),
        ('maybe', '🤔 Maybe, I might recommend it')
    ]

    INFO_CHOICES = [
        ('helpful', '👍 Yes, it was very helpful!'),
        ('not_helpful', '👎 No, it wasn’t helpful.'),
        ('partially_helpful', '🤔 It was somewhat helpful.')
    ]

    INTERFACE_CHOICES = [
        ('intuitive', '👌 Yes, the interface was intuitive'),
        ('confusing', '😕 No, the interface was confusing'),
        ('okay', '🙂 It was okay')
    ]

    USABILITY_CHOICES = [
        ('easy', '✅ Yes, the site was easy to use'),
        ('difficult', '❌ No, the site was difficult to use'),
        ('average', '😐 It was average')
    ]

    PREDICTION_CHOICES = [
        ('accurate', '🎯 Yes, the predictions were accurate'),
        ('inaccurate', '❌ No, the predictions were inaccurate'),
        ('not_sure', '🤷 Not sure')
    ]

    
    predictions_accuracy = forms.ChoiceField(
        label="How accurate were today's predictions?",
        choices=PREDICTION_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )
    
    app_usability = forms.ChoiceField(
        label="Was the app easy to use?",
        choices=USABILITY_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )
    
    user_interface = forms.ChoiceField(
        label="Was the user interface intuitive?",
        choices=INTERFACE_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )
    
    helpful_info = forms.ChoiceField(
        label="Did you find the information provided helpful?",
        choices=INFO_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )
    
    app_recommend = forms.ChoiceField(
        label="Would you recommend this app to others?",
        choices=RECOMMEND_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    def save(self, user=None):
        # Save feedback to the model
        feedback = Feedback(
        user=user,
        predictions_accuracy=self.cleaned_data['predictions_accuracy'],  
        app_usability=self.cleaned_data['app_usability'],
        user_interface=self.cleaned_data['user_interface'],
        helpful_info=self.cleaned_data['helpful_info'],
        app_recommend=self.cleaned_data['app_recommend'],
    )
        feedback.save()
        return feedback