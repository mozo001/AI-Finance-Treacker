from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import Transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
# tracker/views.py
import os
import google.generativeai as genai



def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:index')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username_req = request.POST.get('username')
        password_req = request.POST.get('password')
        user = authenticate(request, username=username_req, password=password_req)
        if user is not None:
            login(request, user)
            return redirect('tracker:index')
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tracker/login.html')

def logout_view(request):
    logout(request)
    return redirect('tracker:login') # FIXED: Namespaced target

@login_required(login_url='tracker:login')
def index(request):
    # Fetch all transactions owned by this user
    all_user_transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Extract all distinct months and years from database entries for form filtering selections
    # Note: If your DB backend doesn't support dates tool natively, alternatives include python set iteration
    available_years = sorted(list(set(t.date.year for t in all_user_transactions)), reverse=True)
    available_months = [
        {'value': i, 'name': timezone.datetime(2000, i, 1).strftime('%B')} for i in range(1, 13)
    ]

    # Pull active configuration parameters out of GET payload
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')

    # Apply date constraints to the ledger execution queries if filters are passed
    filtered_transactions = all_user_transactions
    if selected_year and selected_year.isdigit():
        filtered_transactions = filtered_transactions.filter(date__year=int(selected_year))
    if selected_month and selected_month.isdigit():
        filtered_transactions = filtered_transactions.filter(date__month=int(selected_month))

    # Calculate system totals based strictly on applied context filters
    total_income = filtered_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = filtered_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'transactions': filtered_transactions[:5], # Keeping pagination slice constraint intact
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'balance': float(balance),
        'available_years': available_years,
        'available_months': available_months,
        'selected_year': int(selected_year) if (selected_year and selected_year.isdigit()) else None,
        'selected_month': int(selected_month) if (selected_month and selected_month.isdigit()) else None,
    }
    return render(request, 'tracker/index.html', context)

@login_required(login_url='tracker:login') # FIXED: Namespaced target
def transaction(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    return render(request, 'tracker/mytransaction.html', {'transactions': transactions, 'balance': balance})

@login_required(login_url='tracker:login') # FIXED: Namespaced target
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    return redirect('tracker:transaction')

def categorize_transaction(title):
    title = title.lower()
    if any(word in title for word in ['kfc', 'burger', 'pizza', 'restaurant']):
        return 'food'
    elif any(word in title for word in ['netflix', 'aws', 'render', 'internet']):
        return 'tech'
    else:
        return 'other'

@login_required(login_url='tracker:login') # FIXED: Namespaced target
@login_required(login_url='tracker:login')
def add_transaction(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        date = request.POST.get('date')
        category = categorize_transaction(title) 

        Transaction.objects.create(
            user=request.user, 
            title=title,
            amount=amount,
            transaction_type=transaction_type,
            date=date,
            category=category
        )
        return redirect('tracker:index') 
    return render(request, 'tracker/add_transaction.html') # Render file on GET request

@login_required(login_url='tracker:login') # FIXED: Namespaced target
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.title = request.POST.get('title')
        transaction.amount = request.POST.get('amount')
        transaction.transaction_type = request.POST.get('transaction_type')
        transaction.category = request.POST.get('category')
        transaction.date = request.POST.get('date')
        transaction.description = request.POST.get('description', '')
        transaction.save()

        return redirect('tracker:transaction')

    return render(request, 'tracker/edit_transaction.html', {'transaction': transaction})




# Import your new ML predictor tool
from .predictor import predict_next_month_expense

@login_required(login_url='tracker:login')
def index(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    # 1. Existing Core Calculations
    total_income = user_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = user_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # 2. Trigger the Scikit-Learn Predictive ML
    predicted_expense = predict_next_month_expense(request.user)

    # 3. Trigger the Gemini Generative AI Coach
    ai_analysis = "Add more transaction entries to unlock strict AI budgeting tips."
    
    if user_transactions.exists():
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are a direct, zero-sugar-coating financial coach. Analyze my current numbers:
                Total Income: ${total_income}
                Total Expenses: ${total_expense}
                Net Balance: ${balance}
                Estimated Next Month Single-Day Peak Expense: {predicted_expense}
                
                Give me exactly two sentences of direct, blunt, actionable evaluation about my financial status. Do not compliment me. Be strict.
                """
                response = model.generate_content(prompt)
                ai_analysis = response.text
            except Exception:
                ai_analysis = "AI Coach is currently offline. Verify your Vercel Environment variables."

    context = {
        'transactions': user_transactions[:5], 
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'balance': float(balance),
        'predicted_expense': predicted_expense,  # Pass ML to Template
        'ai_analysis': ai_analysis,              # Pass AI to Template
    }
    return render(request, 'tracker/index.html', context)