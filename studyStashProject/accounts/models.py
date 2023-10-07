
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User
from paymentapp.models import Plan

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    card_details = models.TextField(blank=True, null=True)
    plan = models.ForeignKey('paymentapp.Plan', on_delete=models.SET_NULL, blank=True, null=True)

    groups = models.ManyToManyField(Group, blank=True, related_name='user_accounts')
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',  # Corrected verbose_name
        blank=True,
        related_name='user_accounts_permissions'
    )


    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
