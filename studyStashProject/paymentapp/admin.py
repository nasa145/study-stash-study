

from django.contrib import admin
from .models import Plan, Payment, Subscription

admin.site.register(Plan)
admin.site.register(Payment)
admin.site.register(Subscription)
