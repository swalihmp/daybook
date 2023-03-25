from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Income,Expense,Expenses,Incomes,Doctor,DayClose,Cash_InHand,Doc_op
from django.contrib import messages,auth
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url = 'login')
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
            exp_type = request.POST['type']
            
            exp_name = Expense.objects.get(exp_name = expense)
            user = request.user
            
            time = datetime.now().time()
            
            Expenses.objects.create(user=user,exp=exp_name,amount=amount,date = today,time=time,disc=disc,exp_type=exp_type)
            return redirect('addexp')
        else:
            return redirect('addexp')
    else:
        return redirect('login')



@login_required(login_url = 'login')
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



@login_required(login_url = 'login')
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


@login_required(login_url = 'login')        
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



@login_required(login_url = 'login')    
def doctors(request):
    if request.method == 'POST':
        doc_name = request.POST['doc_name']
        op = request.POST['op']
        disc = request.POST['disc']
        today = request.POST['today']

        user = request.user
        doctor = Doctor.objects.get(doc_name = doc_name)
        
        Doc_op.objects.create(user=user,date=today,doc_name=doctor,opnum=op,disc = disc)
        
        doctors = Doctor.objects.all().order_by('id')
        
        context = {
            'doctors':doctors
        }
        return render(request,'doctorop.html',context)
    else:
        doctors = Doctor.objects.all().order_by('id')
        
        context = {
            'doctors':doctors
        }
        return render(request,'doctorop.html',context)



@login_required(login_url = 'login')    
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
    


@login_required(login_url = 'login')    
def mark(request,id):
    expense = Expenses.objects.get(id=id)

    expense.status=True
    expense.save()
    
    exp = expense.exp
    amount = expense.amount
    disc = expense.disc
    exp_date = expense.date
    
    inc_name = Income.objects.get(inc_name = exp)
    user = request.user
    
    time = datetime.now().time()
    today = datetime.now().date()
    
    Incomes.objects.create(user=user,inc=inc_name,amount=amount,date = today,time=time,disc=disc+","+str(exp_date))
    
    return redirect('HomePage')
    
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



@login_required(login_url = 'login')
def credits(request):
    credit = Expenses.objects.filter(status=False,exp_type='credit')
    context={
        'credit':credit
    }
    return render(request,'credits.html',context)

def cmark(request,id):
    expense = Expenses.objects.get(id=id)

    expense.status=True
    expense.save()
    
    exp = expense.exp
    amount = expense.amount
    disc = expense.disc
    exp_date = expense.date
    
    if Income.objects.filter(inc_name = exp).exists():
        inc_name = Income.objects.get(inc_name = exp)
        user = request.user
        
        time = datetime.now().time()
        today = datetime.now().date()
        
        Incomes.objects.create(user=user,inc=inc_name,amount=amount,date = today,time=time,disc=disc+","+str(exp_date))
        
        return redirect('HomePage')
    else:
        values = Income(
            inc_name = exp
        )
        values.save()
        inc_name = Income.objects.get(inc_name = exp)
        user = request.user
        
        time = datetime.now().time()
        today = datetime.now().date()
        
        Incomes.objects.create(user=user,inc=inc_name,amount=amount,date = today,time=time,disc=disc+","+str(exp_date))
        
        return redirect('credits')


@login_required(login_url = 'login')    
def search(request):
    context={
        'expenses': Expense.objects.all()
    }
    return render(request,'search.html',context)

def search_data(request):
    if request.method=='POST':
        from_date = request.POST['from']
        to_date = request.POST['to']
        expense = request.POST['expense']
        
        exp_name = Expense.objects.get(exp_name = expense)
        
        datas= Expenses.objects.filter(exp = exp_name, date__range = [from_date , to_date],status=False)
        
        total =0
        for i in range(len(datas)):
            x = datas[i].amount
            total = total+int(x)
        
        context={
            'datas':datas,
            'expenses': Expense.objects.all(),
            'total':total,
        }
        return render(request,'search.html',context)
    else:
        return redirect('search')



@login_required(login_url = 'login')    
def dayclose(request):
    if request.method=='POST':
        today = request.POST['today']
        expense = request.POST['expense']
        income = request.POST['income']
        cash_bal = request.POST['cash_bal']
        close_amount = request.POST['close_amount']
        cash_diffrence = request.POST['cash_diffrence']
        
        if DayClose.objects.filter(date=today).exists():
            messages.success(request,'Day Already Closed')
            
            return render(request,'Dayclose.html')
        else:
            DayClose.objects.create(date=today,t_expense=expense,t_income=income,ClosingAmount=cash_bal,CashInhand=close_amount,diffrence=cash_diffrence)
            
            cash_exist = Cash_InHand.objects.all()
            
            if cash_exist:
                my_instance = Cash_InHand.objects.get(id='1')
                cash = my_instance.amount
                
                ex1 = Cash_InHand.objects.filter(id='1').update(
                    amount = int(cash)+int(close_amount)
                )
                
            else:
                my_instance = Cash_InHand(amount=close_amount).save()
            
            return redirect('HomePage')
        
    else:
        return render(request,'Dayclose.html')


@login_required(login_url = 'login')
def daycloseamount(request):
    if request.method=='POST':
        today = request.POST['today']
        twothousand = request.POST['twothousand']
        fivehundred = request.POST['fivehundred']
        twohundred = request.POST['twohundred']
        hundred = request.POST['hundred']
        fifty = request.POST['fifty']
        twenty = request.POST['twenty']
        ten = request.POST['ten']
        coins = request.POST['coins']
    
        total = 2000*int(twothousand)+500*int(fivehundred)+200*int(twohundred)+100*int(hundred)+50*int(fifty)+20*int(twenty)+10*int(ten)+int(coins)
        
        
        today_expense = Expenses.objects.filter(date = today)
        today_income = Incomes.objects.filter(date = today)
        
        today_exp =0
        for i in range(len(today_expense)):
            x = today_expense[i].amount
            today_exp = today_exp+int(x)
            
        today_inc =0
        for i in range(len(today_income)):
            x = today_income[i].amount
            today_inc = today_inc+int(x)
            
        closing_balance = int(today_inc) - int(today_exp)
        
        cash_diff = int(total) - int(closing_balance)
        
        context={
            'total' : total,
            'today_exp' : today_exp,
            'today_inc' : today_inc,
            'closing_balance' : closing_balance,
            'cash_diff' : cash_diff,
            'twothousand' : twothousand,
            'fivehundred': fivehundred,
            'twohundred' : twohundred,
            'hundred' : hundred,
            'fifty' : fifty,
            'twenty' : twenty,
            'ten' : ten,
            'coins' : coins,
            'today': today,
        }
        
        
        return render(request,'Dayclose.html',context)
    else:
        return redirect(dayclose)
    