from django.db import models
from django.contrib.auth.models import User

class Notify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_location = models.CharField(max_length=100)

    def __str__(self):
        return f"Notify preferences for {self.user.username}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional user association
    predictions_accuracy = models.TextField(null=True, blank=True)  # Stores the selected answers as a text list
    app_usability = models.TextField(null=True, blank=True)
    user_interface = models.TextField(null=True, blank=True)
    helpful_info = models.TextField(null=True, blank=True)
    app_recommend = models.TextField(null=True, blank=True)
 

    def __str__(self):
        return f"Feedback from {self.user}" if self.user else "Anonymous Feedback"