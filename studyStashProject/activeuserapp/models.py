
# from django.db import models
# from django.contrib.auth.models import User

# class Task(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     pdf_file = models.FileField(upload_to='task_pdfs/')
#     available_days = models.CharField(max_length=50)  # Store days as a comma-separated list (e.g., "Monday,Sunday")

#     def __str__(self):
#         return self.name


# class Survey(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     pdf_file = models.FileField(upload_to='survey_pdfs/')
#     available_days = models.CharField(max_length=50)  # Store days as a comma-separated list (e.g., "Monday,Sunday")

#     def __str__(self):
#         return self.name
    


# class SurveyResponse(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
#     pdf_file = models.FileField(upload_to='user_survey_responses/')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Response by {self.user.username} to {self.survey.name}"

