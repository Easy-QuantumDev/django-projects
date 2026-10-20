from django.db import models
    


class Category(models.Model):
    
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    category_type = models.CharField(default='income',max_length=10,choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
    

class Transaction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500,blank=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return self.title
    

# Create your models here.
