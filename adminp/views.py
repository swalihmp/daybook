from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.db.models import Q
from datetime import timedelta
from users.models import Expense,Expenses,Income,Incomes,BankDeposit,Cash_InHand,Doctor,Doc_op

from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
import os

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

@login_required(login_url = 'login')
def register(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                username = email.split("@")[0]
                
                user = Account.objects.create_user(first_name = first_name , last_name = last_name, email=email, username=username,password=password)
                user.phone_number = phone_number
                user.save()
                
                
                current_site = get_current_site(request)
                mail_subject = "Pls Activate your Account"
                message = render_to_string('accounts/account_verification_email.html',{
                    'user':user,
                    'domain': current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                
                to_email = email
                send_email = EmailMessage(mail_subject,message, to=[to_email])
                send_email.send()
                
                messages.success(request,'Regetration successful,check email for vertification')
                return redirect("register")
        else:
            form = RegistrationForm()
        context = {
            'form':form,
        }
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account is activated..!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



def login(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin_HomePage')
        else:
            return redirect('HomePage')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            user=auth.authenticate(email=email, password=password)
            
            if user is not None:
                if user.is_admin:
                    auth.login(request,user)
                    return redirect('admin_HomePage')
                else:
                    auth.login(request,user)
                    return redirect('HomePage')
            else:
                messages.error(request, "Invalid Credentials....")
                return redirect('login')
        return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect('login')


@login_required(login_url = 'login')
def credits_p(request):
    if request.user.is_admin:
        credit = Expenses.objects.filter(status=False,exp_type='credit')
        context={
            'credit':credit
        }
        return render(request,'adminp/credit_p.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def patient_p(request):
    if request.user.is_admin:
        exp_name = Expense.objects.get(exp_name='Patient Pending')
        pendings = Expenses.objects.filter(status=False,exp=exp_name)
        context={
            'credit':pendings
        }
        return render(request,'adminp/patient_pendings.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def doctor_report(request):
    if request.user.is_admin:
        if request.method=='POST':
            from_d = request.POST['from']
            to_d = request.POST['to']
            doc_name = request.POST['doc_name']
            
            doc = Doctor.objects.get(doc_name=doc_name)
            doctor = doc.id
            doctorname = doc.doc_name
            
            datas= Doc_op.objects.filter(doc_name=doctor,date__range = [from_d , to_d])
            opsum = datas.aggregate(Sum('opnum'))
            
            total = 0
            for i in range(len(datas)):
                x = datas[i].opnum
                total = total+x


            context={
                'doc': Doctor.objects.all(),
                'doc_report' : datas,
                'doctorname' : doctorname,
                'opsum': total
            }
            return render(request,'adminp/doctor_report.html',context)
        else:
            context={
                'doc': Doctor.objects.all()
            }
            return render(request,'adminp/doctor_report.html',context)
    else:
        return redirect('login')


@login_required(login_url = 'login')    
def admin_search(request):
    if request.user.is_admin:
        context={
            'expenses': Expense.objects.all()
        }
        return render(request,'adminp/search.html',context)
    else:
        return redirect('login')


@login_required(login_url = 'login')    
def admin_search_data(request):
    if request.user.is_admin:
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
            return render(request,'adminp/search.html',context)
        else:
            return redirect('search')
    else:
        return redirect('login')


@login_required(login_url = 'login')    
def admin_HomePage(request):
    if request.user.is_admin:
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
        
        one_month_ago = date - timedelta(days=30)
        monthly_exp = Expenses.objects.filter(date__gte=one_month_ago)
        monthly_inc = Incomes.objects.filter(date__gte=one_month_ago)
        
        monthly_exp_total = 0
        for i in range(len(monthly_exp)):
            x = monthly_exp[i].amount
            monthly_exp_total = monthly_exp_total+int(x)
            
        monthly_inc_total = 0
        for i in range(len(monthly_inc)):
            x = monthly_inc[i].amount
            monthly_inc_total = monthly_inc_total+int(x)
            
        # print(monthly_exp_total)
        # print(monthly_inc_total)
            
        # monthly_report = {'monthly_exp_total':monthly_exp_total,'monthly_inc_total':monthly_inc_total}
        
        context = {
            'today_exp':today_exp,
            'today_inc':today_inc,
            'cash_inhand':cash_inhand,
            'monthly_exp':monthly_exp,
            'monthly_inc' : monthly_inc,
            'monthly_inc_total' :monthly_inc_total,
            'monthly_exp_total' :monthly_exp_total
        }
        
        return render(request,'adminp/admin_home.html',context)
    else:
        return redirect('login')



@login_required(login_url = 'login')
def datewiseexp(request):
    if request.user.is_admin:
        if request.method=='POST':
            from_date = request.POST['from']
            to_date = request.POST['to']
            
            
            datas= Expenses.objects.filter(date__range = [from_date , to_date])
            
            total =0
            for i in range(len(datas)):
                x = datas[i].amount
                total = total+int(x)
            
            context={
                'datas':datas,
                'total':total,
            }
            return render(request,'adminp/datewiseexpense.html',context)
        else:
            return render(request,'adminp/datewiseexpense.html')
    else:
        return redirect('login')


@login_required(login_url = 'login')
def datewiseinc(request):
    if request.user.is_admin:
        if request.method=='POST':
            from_date = request.POST['from']
            to_date = request.POST['to']
            
            
            datas= Incomes.objects.filter(date__range = [from_date , to_date])
            
            total =0
            for i in range(len(datas)):
                x = datas[i].amount
                total = total+int(x)
            
            context={
                'datas':datas,
                'total':total,
            }
            return render(request,'adminp/datewiseincome.html',context)
        else:
            return render(request,'adminp/datewiseincome.html')
    else:
        return redirect('login')
    
    
@login_required(login_url = 'login')
def users(request):
    if request.user.is_superadmin:
        Users=Account.objects.filter(is_admin = False).order_by('id')
        user_count=Users.count()
        context={
            'Users':Users,
            'user_count':user_count,
        }
        return render(request,'adminp/users.html',context)
    else:
        return redirect('login')
    
    
    
@login_required(login_url = 'login')
def blockuser(request,id,action):
    if request.user.is_superadmin:
        user=Account.objects.get(id=id)
        if action=='block':
            user.is_active=False
            user.save()
        elif action =='unblock':
            user.is_active=True
            user.save()

        return redirect('users')
    else:
        return redirect('login')