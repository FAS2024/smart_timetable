from django.contrib import admin
from .models import IdentificationNumber,CustomUser
from django.contrib.auth.admin import UserAdmin




admin.site.register(IdentificationNumber)
admin.site.register(CustomUser)
