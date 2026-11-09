from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import date
from .models import Transaction,Category
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
@login_required
def transaction_list(req):

    transactions = Transaction.objects.select_related('category').all()

    search_query = req.GET.get("q", '')
    if search_query:
        transactions = transactions.filter(title__icontains=search_query)

    category_id = req.GET.get('category', '')
    transaction_type = req.GET.get('type', '')

    if category_id.isdigit():
        transactions = transactions.filter(category_id=category_id)

    if transaction_type in ['income', 'expense']:
        transactions = transactions.filter(
            category__category_type=transaction_type
        )

    # Summary
    income = Transaction.objects.filter(
        category__category_type='income'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    expenses = Transaction.objects.filter(
        category__category_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    balance = income - expenses

    total_transactions = Transaction.objects.count()

    recent_transactions = Transaction.objects.select_related(
        'category'
    ).order_by('-created_at')[:5]

    # Monthly transactions
    monthly_data = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month', 'category__category_type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Last 6 months
    today = timezone.localdate()
    months = []

    for i in range(5, -1, -1):
        current_month = today.month - i
        current_year = today.year

        while current_month <= 0:
            current_month += 12
            current_year -= 1

        months.append(date(current_year, current_month, 1))

    # Chart data
    chart_labels = []
    chart_income = []
    chart_expenses = []

    for current_month in months:
        income_amount = Decimal('0.00')
        expense_amount = Decimal('0.00')

        for item in monthly_data:
            item_month = item['month'].date()

            if item_month == current_month:
                if item['category__category_type'] == 'income':
                    income_amount = item['total']

                elif item['category__category_type'] == 'expense':
                    expense_amount = item['total']

        chart_labels.append(current_month.strftime('%B %Y'))
        chart_income.append(float(income_amount))
        chart_expenses.append(float(expense_amount))

    # Context
    context = {
        'transactions': transactions,
        'total_income': income,
        'total_expenses': expenses,
        'balance': balance,
        'categories': Category.objects.all(),
        'search_query': search_query,
        'category_id': category_id,
        'transaction_type': transaction_type,
        'total_transactions': total_transactions,
        'recent_transactions': recent_transactions,
        'chart_labels': chart_labels,
        'chart_income': chart_income,
        'chart_expenses': chart_expenses,
    }

    return render(req, 'transactions.html', context)
@login_required
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
@login_required
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

@login_required(login_url='accounts:login')
def delete_transaction(req,pk):
    transaction = get_object_or_404(Transaction,pk=pk)
    if req.method == 'POST':
        transaction.delete()
        return redirect("expenses:transaction-list")    
    return redirect("expenses:transaction-list")


    


# Create your views here.


