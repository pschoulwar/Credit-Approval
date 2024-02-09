from django.db import models
from django.utils import timezone
from loanapp.models import Loan, Customers

def calculate_credit_score_from_loans(customer_id):
    total_percentage_paid_on_time = 0
    total_loans = 0
    has_ongoing_loans = False
    credit_score = 0
    
    
    customer = Customers.objects.get(customer_id=customer_id)
    monthly_salary = customer.monthly_salary
    loan_limit = monthly_salary * 36
    
    
    total_loan_amount = Loan.objects.filter(customer_id=customer_id).aggregate(total_loan_amount=models.Sum('loan_amount'))['total_loan_amount']
    if total_loan_amount >= loan_limit:
        return 0
    
    loan_ids = Loan.objects.filter(customer_id=customer_id).values_list('loan_id', flat=True)
    for loan_id in loan_ids:
        loan = Loan.objects.get(loan_id=loan_id)
        
        end_date = loan.end_date
        emis_status = (end_date - timezone.now().date()).days 
        total_emi = emis_status
        emi_on_time = loan.emis_paid_on_time
        percentage_paid = (emi_on_time / total_emi) * 100 if total_emi != 0 else 0
        
        total_percentage_paid_on_time += percentage_paid
        total_loans += 1
        
        
        if end_date > timezone.now().date():
            has_ongoing_loans = True
    
    average_percentage_paid_on_time = total_percentage_paid_on_time / total_loans if total_loans != 0 else 0   
    
    
    if Loan.objects.filter(customer_id=customer_id, end_date__lt=timezone.now().date()).exists():
        credit_score += 30
    else:
        credit_score += 0
    
    
    if has_ongoing_loans:
        credit_score += 40
    if average_percentage_paid_on_time > 70:
        credit_score += 30
    
    return credit_score
