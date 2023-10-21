from django.contrib import admin
from .models import Task, DownloadedTask, SubmmittedTasks

# Register your models here.
admin.site.register(Task)
admin.site.register(DownloadedTask)
admin.site.register(SubmmittedTasks)
