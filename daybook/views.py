from django.shortcuts import render
from datetime import datetime
from users.models import Expenses,Incomes,Expense

# Create your views here.

# def custom_404(request, exception=None):
#     return render(request, '404.html')


def HomePage(request):
    date = datetime.now().date()
    
    today_expense = Expenses.objects.filter(date = date)
    today_income = Incomes.objects.filter(date = date)
    
    today_exp =0
    for i in range(len(today_expense)):
        x = today_expense[i].amount
        today_exp = today_exp+int(x)
    
    
    today_inc =0
    for i in range(len(today_income)):
        x = today_income[i].amount
        today_inc = today_inc+int(x)
        
    exp_name = Expense.objects.get(exp_name='Patient Pending')
    pendings = Expenses.objects.filter(status=False,exp=exp_name)
    
    
    context = {
        'today_expense':today_expense,
        'today_income':today_income,
        'today_exp':today_exp,
        'today_inc':today_inc,
        'pendings':pendings
    }
    
    return render(request,'homepage.html',context)
