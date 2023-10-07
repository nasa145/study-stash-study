
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Plan(models.Model):
     name = models.CharField(max_length=255)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     rewards_description = models.TextField()

     def __str__(self):
         return self.name



class Subscription(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
     is_active = models.BooleanField(default=True)

     def __str__(self):
         return f"{self.user.username}'s {self.plan.name} Plan"
    


# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.user.username}'s Payment for {self.plan.name}"