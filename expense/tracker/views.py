from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def index(request):

    if request.method == "POST":
        print(request.POST)
        form = request.POST
        description = form.get('description')
        amount = form.get('amount')
        
        if not description or amount:
            return redirect('/')

        print(description,amount)
    
    return render(request, 'index.html')