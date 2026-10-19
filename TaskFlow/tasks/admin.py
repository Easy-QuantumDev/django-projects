from django.contrib import admin
from .models import Task
class Admin_model(admin.ModelAdmin):
    list_display = ['title','is_completed']
    search_fields = ['title']



admin.site.register(Task)




# Register your models here.
