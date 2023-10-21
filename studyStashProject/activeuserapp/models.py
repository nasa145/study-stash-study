
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='task_pdfs/')
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField()
    task_completion_reward = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.title


class DownloadedTask(models.Model):
    user = models.ForeignKey('accounts.ApplicationUser', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date_Downloaded = models.DateTimeField(default=timezone.now)
    uploaded_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} downloaded the task {self.task.title}"
    


class SubmmittedTasks(models.Model):

    APPROVAL_STATUS = (
        ('PENDING', 'PENDING'),
        ('REJECTED', 'REJECTED'),
        ('ACCEPTED', 'ACCEPTED'),
    )

    PAID_STATUS = (
        ('PAID', 'PAID'),
        ('NOT_PAID', 'NOT PAID')
    )

    user = models.ForeignKey('accounts.ApplicationUser', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='user_task_submision/')
    submitted_date = models.DateTimeField(default=timezone.now)
    approvalStatus = models.CharField(max_length=100, choices=APPROVAL_STATUS, default='PENDING')
    paidStatus = models.CharField(max_length=100, choices=PAID_STATUS , default='NOT_PAID')
    amount_to_be_paid_as_reward = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Task Submission by {self.user.username} to {self.task.name}"

