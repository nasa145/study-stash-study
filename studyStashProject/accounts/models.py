

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class ApplicationUser(AbstractUser):
    registered_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey('paymentapp.Plan', on_delete=models.SET_NULL, blank=True, null=True)  # Use Plan directly

    groups = models.ManyToManyField(Group, blank=True, related_name='user_accounts')
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='user_accounts_permissions'
    )

    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    user = models.OneToOneField(ApplicationUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    total_amount_earned_from_site =  models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.user.username
