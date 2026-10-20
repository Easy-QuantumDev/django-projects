from django.contrib import admin
from .models import Transaction,Category

class transactionModel(admin.ModelAdmin):
    list_display = ['title','created_at','amount','category']
    search_fields = ['title']
    list_filter = ['category','created_at']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type']
    search_fields = ['name']
    list_filter = ['category_type']

admin.site.register(Transaction,transactionModel)    

admin.site.register(Category,CategoryAdmin)    

# Register your models here.
