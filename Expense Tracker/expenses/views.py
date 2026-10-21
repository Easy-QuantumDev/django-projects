from django.shortcuts import render,redirect,get_object_or_404
from .models import Transaction,Category
from django.contrib import messages
def transaction_list(req):
    transactions = Transaction.objects.select_related('category').all()
    return render(req,'transactions.html',{'transactions':transactions})
def create_transaction(req):
    categories = Category.objects.all()
    if req.method =='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        amount = req.POST.get('amount')
        if not title:
            messages.error(req,'Title is required')
            return redirect('expenses:create-list')

        if not amount:
            messages.error(req,'Amount is required')
            return redirect('expenses:create-list')

        try:
            category_id = req.POST.get('category')
            category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(req,'create_transaction.html',{'error': 'Category does not exist'})        
            
        transaction = Transaction.objects.create(title=title,description=description,amount=amount,category=category_obj)
         
        return redirect('expenses:transaction-list')        
            
    return render(req,'create_transaction.html',{'categories':categories})        

def edit_transaction(req,pk):
    transaction = get_object_or_404(Transaction,id=pk)
    categories = Category.objects.all()
    
    if req.method == 'POST':
        category_id = req.POST.get("category")
        category_obj = Category.objects.get(id=category_id)
            
        title = req.POST.get("title")
        
        description = req.POST.get("description")
        
        amount = req.POST.get("amount")
        
        transaction.title = title
        transaction.description = description
        transaction.amount = amount
        transaction.category = category_obj
        transaction.save()
        
        return render(req,'edit_transaction.html',{"message":'transaction edit successfully '})
        
    return render(req,'edit_transaction.html',{"transaction":transaction,'categories':categories})



    


# Create your views here.


