from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Income,Expense,Expenses,Incomes,Doctor
from django.contrib import messages,auth
from django.db.models import Q
from datetime import datetime


# Create your views here.
def addexp(request):
    date = datetime.now().date()
    expenses = Expenses.objects.filter(date=date).order_by('id')
    expense = Expense.objects.all()
    context = {
        'expense':expense,
        'expenses':expenses
    }
    return render(request,'addexp.html',context)

def add_exp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            expense = request.POST['expense']
            amount = request.POST['amount']
            disc = request.POST['disc']
            today = request.POST['today']
            
            exp_name = Expense.objects.get(exp_name = expense)
            user = request.user
            
            time = datetime.now().time()
            
            Expenses.objects.create(user=user,exp=exp_name,amount=amount,date = today,time=time,disc=disc)
            return redirect('addexp')
        else:
            return redirect('addexp')
    else:
        return redirect('login')

def addincome(request):
    date = datetime.now().date()
    incomes = Incomes.objects.filter(date=date).order_by('id')
    income = Income.objects.all()
    context = {
        'income':income,
        'incomes':incomes
    }
    return render(request,'addincome.html',context)

def add_inc(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            income = request.POST['income']
            amount = request.POST['amount']
            disc = request.POST['disc']
            today = request.POST['today']
            
            inc_name = Income.objects.get(inc_name = income)
            user = request.user
            
            time = datetime.now().time()
            
            Incomes.objects.create(user=user,inc=inc_name,amount=amount,date = today,time=time,disc=disc)
            return redirect('addincome')
        else:
            return redirect('addincome')
    else:
        return redirect('login')

def new_income(request):
    if request.method == 'POST':
        if Income.objects.filter(inc_name = request.POST['inc_name']).exists():
            messages.error(request, "Income already exist...!")
            return render(request, 'addincome.html')
        else:
            values = Income(
                inc_name = request.POST['inc_name']
            )
            values.save()
            return redirect('addincome')
    else:
        return redirect('addincome')
        
def new_exp(request):
    if request.method == 'POST':
        if Expense.objects.filter(exp_name = request.POST['exp_name']).exists():
            messages.error(request, "Expense already exist...!")
            return render(request, 'addexp.html')
        else:
            values = Expense(
                exp_name = request.POST['exp_name']
            )
            values.save()
            return redirect('addexp')
    else:
        return redirect('addexp')
    
def doctors(request):
    doctors = Doctor.objects.all().order_by('id')
    
    context = {
        'doctors':doctors
    }
    return render(request,'doctorop.html',context)
    
def new_doc(request):
    if request.method == 'POST':
        if Doctor.objects.filter(doc_name = request.POST['doc_name']).exists():
            messages.error(request, "Doctor already exist...!")
            return render(request, 'doctorop.html')
        else:
            values = Doctor(
                doc_name = request.POST['doc_name']
            )
            values.save()
            return redirect('doctors')
    else:
        return redirect('doctors')
    
# def add_inc(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             income = request.POST['income']
#             amount = request.POST['amount']
#             disc = request.POST['disc']
#             today = request.POST['today']
            
#             inc_name = Income.objects.get(inc_name = income)
#             user = request.user
            
#             time = datetime.now().time()
            
#             Incomes.objects.create(user=user,inc=inc_name,amount=amount,date = today,time=time,disc=disc)
#             return redirect('addincome')
#         else:
#             return redirect('addincome')
#     else:
#         return redirect('login')