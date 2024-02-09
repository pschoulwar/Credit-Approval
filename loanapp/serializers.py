from rest_framework import serializers
from .models import Customers
from .models import Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['first_name', 'last_name', 'phone_number', 'monthly_salary']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment']
