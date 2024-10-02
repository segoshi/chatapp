from django.contrib import admin

# Register your models here.
from .models import CustomUser, Talk

admin.site.register(CustomUser)
admin.site.register(Talk)