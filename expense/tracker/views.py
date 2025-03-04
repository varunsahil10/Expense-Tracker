from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from tracker.models import *
from decimal import Decimal
from django.db.models import Sum
# Create your views here.
def index(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        form = request.POST
        description = form.get('description')
        amount = form.get('amount')
        
        if not description and not amount:
            messages.info(request, "Description or amount can't be blank.")
            return redirect('/')
            
        Transaction.objects.create(
            description = description,
            amount = Decimal(amount)
        )

    transactions = Transaction.objects.all()

    context.update({
        'transactions': transactions,
        'balance': transactions.aggregate(balance = Sum('amount')).get('balance',0.00) or 0.00,
        'income': transactions.filter(amount__gte=0).aggregate(income = Sum('amount')).get('income',0.00) or 0.00,
        'expense': transactions.filter(amount__lt = 0).aggregate(expense = Sum('amount')).get('expense',0.00) or 0.00,
    })

    print(context)

    
    return render(request, 'index.html',context)


def deleteTransaction(request, id):
    transaction = Transaction.objects.get(id=id)
    if transaction:
        transaction.delete()
    return render('/')