from django.http import HttpRequest

from autho.models import StaffUser, User
from django.db.models import Count

from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from common.api_response import api_response_error, api_response_success
from common.mixins import BaseApiMixin
from autho.serializers import StaffUserSerializer, UserSerializer
from cooperative.models import LoanAccount

# Create your views here.


class UserViewSet(BaseApiMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ["first_name", "last_name", "phone_number", "loans__account_number", "loans__finance__idx"]



    @action(detail=False, methods=["GET"])
    def user_account_summary(self, request):

        user_loan_accounts = LoanAccount.objects.all()

        loan_accounts_list = []
        for loan_account in user_loan_accounts:
            finance_name = loan_account.finance.name
            for loan_account_item in loan_accounts_list:
                if loan_account_item["finance_name"] == finance_name:
                    loan_account_item["total_amount"] += loan_account.total_loan
                    loan_account_item["outstanding"] += loan_account.loan_outstanding
                    loan_account_item["overdue_amount"] += loan_account.overdue_amount
                    loan_account_item["total_account"] += 1
                    break
            else:
                loan_accounts_list.append(
                    {
                        "finance_name": finance_name,
                        "total_amount": loan_account.total_loan,
                        "outstanding": loan_account.loan_outstanding,
                        "overdue_amount": loan_account.overdue_amount,
                        "total_account": 1
                    }
                )

        return api_response_success(loan_accounts_list)
    

    @action(detail=False, methods=["GET"])
    def user_loan_type(self, request):
        user_idx = request.query_params.get('user')
        if not user_idx:
            return api_response_error("User ID is required", status=400)
        
        type_counts = LoanAccount.objects.filter(user__idx=user_idx).values('loan_nature').annotate(count=Count('loan_nature'))
        
        results = {loan_type: 0 for loan_type, _ in LoanAccount.NATURE_CHOICES}

        for type_count in type_counts:
            results[type_count['loan_nature']] = type_count['count']
        
        return api_response_success(results)
    
    @action(detail=False, methods=["GET"])
    def user_account(self, request):
        user_loan_accounts = LoanAccount.objects.all()  # Adjust the query as needed

        user_account_list = [
            {
                "user_idx": user_account.user.idx,  # Assuming user is a ForeignKey field in UserLoanAccount
                "number_of_account": user_account.account_number,
                "type_of_loan": user_account.loan_type,
                "finance_name": user_account.finance.name,
                "outstanding_balance": user_account.loan_outstanding,
                "utilization_percent_credit": user_account.utilization_percent,
                "amount_overdue": user_account.total_loan - user_account.total_paid
            }
            for user_account in user_loan_accounts
        ]

        return api_response_success(user_account_list)


class StaffUserViewSet(BaseApiMixin, ModelViewSet):
    queryset = StaffUser.objects.all()
    serializer_class = StaffUserSerializer

    @action(detail=False, methods = ['GET', 'PATCH'])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    

    @action(detail=False, methods=["POST"])
    def change_password(self, request: HttpRequest) -> Response:

        if not request.user.is_authenticated:
            return api_response_error(
                {"detail": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        user: StaffUser = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        is_correct = user.check_password(old_password)
        if is_correct:
            if not new_password:
                return api_response_error(
                    {"detail": "New password cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
            user.save()
            return api_response_success(
                {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
            )
        else:
            return api_response_error(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    


class TokenObtainPairView(TokenObtainPairView):
    # permission_classes = ([BazraPermission])
    pass


class TokenRefreshView(TokenRefreshView):
    # permission_classes = ([BazraPermission])
    pass


class TokenVerifyView(TokenVerifyView):
    # permission_classes = ([BazraPermission])
    pass

