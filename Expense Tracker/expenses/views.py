from django.shortcuts import render,redirect
from .models import Transaction,Category

def transaction_list(req):
    transactions = Transaction.objects.select_related('category').all()
    return render(req,'transactions.html',{'transactions':transactions})
def create_transaction(req):
    categories = Category.objects.all()
    if req.method =='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        amount = req.POST.get('amount')
        try:
            category_id = req.POST.get('category')
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(req,'create_transaction.html',{'error': 'Category does not exist'})        
            
        transaction = Transaction.objects.create(title=title,description=description,amount=amount,category=category_obj)
         
        return redirect('expenses:transaction-list')        
            
    return render(req,'create_transaction.html',{'categories':categories})        
# Create your views here.
