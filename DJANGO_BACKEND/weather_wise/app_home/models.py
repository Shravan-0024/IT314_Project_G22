<<<<<<< HEAD
from django.db import models
=======
from django.db import models
from django.contrib.auth.models import User

class Notify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_location = models.CharField(max_length=100)

    def __str__(self):
        return f"Notify preferences for {self.user.username}"
>>>>>>> 256e932 (Notify_model)
