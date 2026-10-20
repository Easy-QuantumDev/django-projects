from django.urls import path
from .views import transaction_list,create_transaction
app_name = 'expenses'
urlpatterns = [
    path('',transaction_list,name = 'transaction-list'),
    path('create/',create_transaction,name = 'create-list'),
]
