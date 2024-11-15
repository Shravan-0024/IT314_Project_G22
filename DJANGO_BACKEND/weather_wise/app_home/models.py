from django.db import models
from django.contrib.auth.models import User

class Notify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_location = models.CharField(max_length=100)

    def __str__(self):
        return f"Notify preferences for {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional user association

    PREDICTION_CHOICES = [
        ('accurate', 'Yes, the predictions were accurate'),
        ('inaccurate', 'No, the predictions were inaccurate'),
        ('not_sure', 'Not sure')
    ]
    USABILITY_CHOICES = [
        ('easy', 'Yes, the app was easy to use'),
        ('difficult', 'No, the app was difficult to use'),
        ('average', 'It was average')
    ]
    INTERFACE_CHOICES = [
        ('intuitive', 'Yes, the interface was intuitive'),
        ('confusing', 'No, the interface was confusing'),
        ('okay', 'It was okay')
    ]
    INFO_CHOICES = [
        ('helpful', 'Yes, the information provided was helpful'),
        ('not_helpful', 'No, the information was not helpful'),
        ('partially_helpful', 'It was partially helpful')
    ]
    RECOMMEND_CHOICES = [
        ('yes', 'Yes, I would recommend this app'),
        ('no', 'No, I would not recommend it'),
        ('maybe', 'Maybe, I might recommend it')
    ]

    predictions_accuracy = models.CharField(max_length=20, choices=PREDICTION_CHOICES, null=True, blank=True)
    app_usability = models.CharField(max_length=20, choices=USABILITY_CHOICES, null=True, blank=True)
    user_interface = models.CharField(max_length=20, choices=INTERFACE_CHOICES, null=True, blank=True)
    helpful_info = models.CharField(max_length=20, choices=INFO_CHOICES, null=True, blank=True)
    app_recommend = models.CharField(max_length=20, choices=RECOMMEND_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Feedback from {self.user}" if self.user else "Anonymous Feedback"
