from django.db import models
from django.contrib.auth.models import User
# Create your models here.

REGION_CHOICES = [
    ('Northeast', 'Northeast'),
    ('Southeast', 'Southeast'),
    ('Midwest', 'Midwest'),
    ('Southwest', 'Southwest'),
    ('West', 'West'),
    ('International', 'International'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, default='Northeast')

    def __str__(self):
        return self.user.username + " - " + self.region
