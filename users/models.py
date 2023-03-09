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
    doc_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    opnum = models.IntegerField(null=False)
    