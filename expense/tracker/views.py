from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from tracker.models import *
from decimal import Decimal
from django.db.models import Sum
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from pprint import pprint
# Create your views here.
# login_url_rev = reverse('login')
@login_required
def index(request):
    
    # pprint(request.__dict__)
    # print(request.user.username)
    # print(request.user.password)

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
            amount = Decimal(amount),
            user = request.user
        )

    transactions = Transaction.objects.filter(user=request.user)

    context.update({
        'transactions': transactions,
        'balance': transactions.aggregate(balance = Sum('amount')).get('balance',0.00) or 0.00,
        'income': transactions.filter(amount__gte=0).aggregate(income = Sum('amount')).get('income',0.00) or 0.00,
        'expense': transactions.filter(amount__lt = 0).aggregate(expense = Sum('amount')).get('expense',0.00) or 0.00,
    })

    print(context)

    
    return render(request, 'index.html',context)


@login_required
def deleteTransaction(request, id):
    transaction = Transaction.objects.get(id=id)
    if transaction:
        transaction.delete()
    return redirect(reverse('index'))


#user registration
def sign_up(request):
    form = SignupForm()
    if request.method == 'POST':
        # print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            print('form is valid')
            data = form.cleaned_data
            email = data.get('email')
            if User.objects.filter(email=email).exists():
                print(f"email already exists for {email}")
                messages.error(request, "email already exists")
                return redirect(reverse('signup'))
            messages.success(request,'Account created successfully!')
            form.save()
        else:
            messages.error(request,'Error occured!')

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


#user login
def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            print('form is valid')
            data = form.cleaned_data
            uname = data.get('username')
            upass = data.get('password')

            print(uname, upass)

            user = authenticate(username=uname, password = upass)
            print(user)

            login(request,user)
            messages.success(request,"user logged in successfully!")
            return redirect(reverse('index'))
        
        else:
            messages.error(request,"Invalid credentials!")
            return redirect(reverse('login'))


    context = {
        'form': form,
    }

    return render(request, 'userlogin.html', context)


#user login
def user_logout(request):
    print(request.user)

    logout(request)
    messages.success(request,"user logged out successfully!")
    return redirect(reverse('login'))


