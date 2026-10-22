from django.urls import path
from .views import transaction_list,create_transaction,edit_transaction,delete_transaction
app_name = 'expenses'
urlpatterns = [
    path('',transaction_list,name = 'transaction-list'),
    path('create/',create_transaction,name = 'create-list'),
    path('edit/<int:pk>/',edit_transaction,name = 'edit-transaction'),
    path('delete/<int:pk>/',delete_transaction,name = 'delete-transaction'),
    
    
]
