from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Notify,Feedback

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-700 rounded-md text-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-700 rounded-md text-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-700 rounded-md text-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        # Add Bootstrap class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered. Please log in instead.")
        return email



class UserProfileEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        # Make username read-only since it's generally not editable
        self.fields['username'].widget.attrs['readonly'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email address is already registered with another account.")
        return email

class NotifyForm(forms.ModelForm):
    get_notifications = forms.BooleanField(required=False, label="Receive Notifications")
    preferred_location = forms.CharField(max_length=100, required=False, label="Preferred Location")

    class Meta:
        model = Notify
        fields = ['preferred_location']

    def clean(self):
        cleaned_data = super().clean()
        get_notifications = cleaned_data.get('get_notifications')
        preferred_location = cleaned_data.get('preferred_location')

        # Validation logic
        if not get_notifications and preferred_location:
            raise ValidationError("You need to enable notifications to have a preferred location.")
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
            predictions_accuracy=', '.join(self.cleaned_data['predictions_accuracy']),
            app_usability=', '.join(self.cleaned_data['app_usability']),
            user_interface=', '.join(self.cleaned_data['user_interface']),
            helpful_info=', '.join(self.cleaned_data['helpful_info']),
            app_recommend=', '.join(self.cleaned_data['app_recommend'])
        )
        feedback.save()
        return feedback