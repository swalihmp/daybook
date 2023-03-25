from django.db import models
from adminp.models import Account 


class Expense(models.Model):
    exp_name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.exp_name
    
class Income(models.Model):
    inc_name = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.inc_name
    
class Expenses(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    exp = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50,null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    disc = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=False)
    exp_type = models.CharField(max_length=20,default="exp",null=False)
    
class Incomes(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    inc = models.ForeignKey(Income, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50,null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    disc = models.CharField(max_length=100,null=True)
    
class Doctor(models.Model):
    doc_name = models.CharField(max_length=100 , null=False)
    
    def __str__(self):
        return self.doc_name
    
class Doc_op(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    doc_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    opnum = models.IntegerField(null=False)
    disc = models.CharField(max_length=10,null=False)
    
class DayClose(models.Model):
    date = date = models.DateField(null=False)
    t_expense = models.BigIntegerField(null=False)
    t_income = models.BigIntegerField(null=False)
    ClosingAmount = models.BigIntegerField(null=False)
    CashInhand = models.BigIntegerField(null=False)
    diffrence = models.BigIntegerField(null=False)
    
class Cash_InHand(models.Model):
    amount = models.BigIntegerField(null=False)
    
class BankDeposit(models.Model):
    today = models.DateField()
    deposite = models.BigIntegerField(null=False)
    disc = models.CharField(max_length=50)