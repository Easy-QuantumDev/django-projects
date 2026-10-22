from django.shortcuts import render,redirect,get_object_or_404
from .models import Transaction,Category
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal

def transaction_list(req):
    transactions = Transaction.objects.select_related('category').all()

    income = Transaction.objects.filter(
        category__category_type='income'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    expenses = Transaction.objects.filter(
        category__category_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    balance = income - expenses

    context = {
        'transactions': transactions,
        'total_income': income,
        'total_expenses': expenses,
        'balance': balance,
    }

    return render(req, 'transactions.html', context)

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
        
        return redirect("expenses:transaction-list")        
    return render(req,'edit_transaction.html',{"transaction":transaction,'categories':categories})

def delete_transaction(req,pk):
    transaction = get_object_or_404(Transaction,pk=pk)
    if req.method == 'POST':
        transaction.delete()
        return redirect("expenses:transaction-list")    
    return redirect("expenses:transaction-list")


    


# Create your views here.


