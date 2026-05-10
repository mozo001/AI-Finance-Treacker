from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Sum
from .models import Transaction
# Create your views here.
def index(request):
    return render (request, 'index.html')


def transaction(request):
    # Fetch all transactions from the database
    transactions = Transaction.objects.all().order_by('-date')
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    # Send them to the template
    return render(request, 'mytransaction.html', {'transactions': transactions, 'balance': balance})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transaction')


def categorize_transaction(title):

    title = title.lower()

    if any(word in title for word in ['kfc', 'burger', 'pizza', 'restaurant']):
        return 'food'
    elif any(word in title for word in ['netflix', 'aws', 'render', 'internet']):
        return 'tech'
    else:
        return 'other'
    
def add_transaction(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        category = categorize_transaction(title)
        Transaction.objects.create(
            title=title,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            date=date,
            description=description,
        )
        return redirect('transaction')

    return render(request, 'add_transaction.html')

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        transaction.save()

        return redirect('transaction')

    return render(request, 'edit_transaction.html',{'transaction': transaction})