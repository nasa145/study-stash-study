
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rewards_description = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey('accounts.ApplicationUser', on_delete=models.CASCADE)  # Import ApplicationUser from the accounts app
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_subscribeed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s {self.plan.name} Plan"
    


class Payment(models.Model):
    user = models.ForeignKey('accounts.ApplicationUser', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, default=1)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return f"{self.user.username}'s Payment for {self.plan.name}"