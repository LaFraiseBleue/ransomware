from django.contrib import admin

# Register your models here.
from .models import SimpleDatas

class SimpleDatasAdmin(admin.ModelAdmin):
    list_display = ('client_adress', 'host','uuid')


admin.site.register(SimpleDatas, SimpleDatasAdmin)