from django.urls import path
from .views import *

urlpatterns = [
    path('register/',CustomerRegistrationAPIView.as_view(), name='register_customer'),
    path('check-eligibility/',LoanEligibilityCheckAPIView.as_view()),
    path('creat-loan/',CreateLoanAPIView.as_view()),
    path('view-loan/<int:loan_id>/', ViewLoanAPIView.as_view(), name='view_loan'),
    path('view-loans/<int:customer_id>/', GetallLoansAPIview.as_view(), name='view_customer_loans')
    
]
