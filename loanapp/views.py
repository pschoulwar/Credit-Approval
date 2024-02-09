from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer
from .models import Customers
from .credit_score import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Loan
from django.shortcuts import get_object_or_404
from .serializers import *


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    if loan_amount is None or interest_rate is None or tenure is None:
        return None  

    interest_rate_percentage = interest_rate / 100
    monthly_installment = (loan_amount + (interest_rate_percentage * loan_amount)) / tenure
    return monthly_installment

class CustomerRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            monthly_salary = int(serializer.validated_data['monthly_salary'])
            serializer.validated_data['approved_limit'] = round(monthly_salary * 36 , -5)
            customer = serializer.save()
            
            response_data = {
                'customer_id' : customer.customer_id,
                'name' : f"{customer.first_name} {customer.last_name}",
                'monthly_salary' : customer.monthly_salary,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
                
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
            
class LoanEligibilityCheckAPIView(APIView):
    def post(self, request):
        
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        tenure = request.data.get('tenure')
        monthly_salary = request.data.get('monthly_salary')
        
        
        credit_score = calculate_credit_score_from_loans(customer_id)
        
        interest_rate = None
        if credit_score > 50:
            interest_rate = 8  
        elif 50 > credit_score > 30:
            interest_rate = 12  
        elif 30 > credit_score > 10:
            interest_rate = 16  
        
    
        if interest_rate is not None:
            monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
        else:
            monthly_installment = None
        
        
        remaining_income = monthly_salary - monthly_installment
        
        can_loan_be_approved = interest_rate is not None and monthly_installment is not None and remaining_income > 0
        
        return Response({
            'customer_id': customer_id,
            'can_loan_be_approved': can_loan_be_approved,
            'interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment
        })

class CreateLoanAPIView(APIView):
    def post(self, request):
        
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        tenure = request.data.get('tenure')
        
        
        eligibility_check_api = LoanEligibilityCheckAPIView()
        eligibility_response = eligibility_check_api.post(request)
        
        
        can_loan_be_approved = eligibility_response.data['can_loan_be_approved']
        interest_rate = eligibility_response.data['interest_rate']
        
        if can_loan_be_approved:
            
            monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
            
            # Save loan details to the database
            loan = Loan.objects.create(customer_id=customer_id, loan_amount=loan_amount, tenure=tenure, interest_rate=interest_rate)
            
            
            loan.monthly_installment = monthly_installment
            loan.save()
            
            
            response_data = {
                'loan_id': loan.id,
                'customer_id': customer_id,
                'loan_approved': True,
                'monthly_installment': monthly_installment
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            
            message = "Loan approval not possible based on credit score and eligibility criteria."
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
  

class ViewLoanAPIView(APIView):
    def get(self, request, loan_id):
        
        loan = get_object_or_404(Loan, loan_id=loan_id)


        customer_name = f"{loan.customer.first_name} {loan.customer.last_name}"
    
        loan_amount = loan.loan_amount
        tenure = loan.tenure
        interest_rate = loan.interest_rate
        monthly_installment = loan.monthly_installment

        # Construct the response data
        response_data = {
            'customer_name': customer_name,
            'loan_amount': loan_amount,
            'tenure': tenure,
            'interest_rate': interest_rate,
            'monthly_installment': monthly_installment
        }

        return Response(response_data)

class GetallLoansAPIview(APIView):
    def get(self, request, customer_id):
        try:
            loans = Loan.objects.filter(customer_id=customer_id)
            serializer = LoanSerializer(loans, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)