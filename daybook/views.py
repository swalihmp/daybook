from django.shortcuts import render,redirect
from datetime import datetime
from users.models import Expenses,Incomes,Expense,Cash_InHand,BankDeposit

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
        
    cash_inhand = Cash_InHand.objects.get(id='1')
    
    exp_name = Expense.objects.get(exp_name='Patient Pending')
    pendings = Expenses.objects.filter(status=False,exp=exp_name)
    
    
    context = {
        'today_expense':today_expense,
        'today_income':today_income,
        'today_exp':today_exp,
        'today_inc':today_inc,
        'pendings':pendings,
        'cash_inhand':cash_inhand
    }
    
    return render(request,'homepage.html',context)

def bank_deposit(request):
    if request.method == 'POST':
        today =request.POST['today']
        deposite =request.POST['amount']
        disc = request.POST['disc']
        
        BankDeposit.objects.create(today=today,deposite=deposite,disc=disc)
        
        my_instance = Cash_InHand.objects.get(id='1')
        cash = my_instance.amount
        
        ex1 = Cash_InHand.objects.filter(id='1').update(
            amount = int(cash)-int(deposite)
        )
        return redirect('HomePage')