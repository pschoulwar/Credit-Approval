from django.db import models

# Create your models here.
class Customers(models.Model):
    customer_id = models.AutoField(primary_key =True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default = 18)
    phone_number = models.BigIntegerField()
    monthly_salary = models.BigIntegerField()
    approved_limit = models.BigIntegerField()
    # current_debt = models.IntegerField(default =0)
    # credit_score = models.IntegerField(default=0)

class Loan(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key =True)
    loan_amount = models.IntegerField()  
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = models.IntegerField()  
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
