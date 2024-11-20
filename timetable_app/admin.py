from django.contrib import admin
from .models import IdentificationNumber

@admin.register(IdentificationNumber)
class MatricNumberAdmin(admin.ModelAdmin):
    list_display = ['identification_number']

