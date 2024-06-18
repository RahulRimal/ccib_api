from rest_framework import serializers

from autho.models import User
from autho.serializers import UserSerializer, UserSerializer
from common.helpers import generate_random_number, generate_username
from common.mixins import BaseModelSerializerMixin
from cooperative.models import (
    Blacklist,
    BlacklistReport,
    Company,
    Finance,
    FinanceStaff,
    FinanceUser,
    Inquiry,
    Installment,
    LoanAccount,
    LoanApplication,
    PersonalGuarantor,
    SecurityDeposit,
)



class FinanceUserSerializer(BaseModelSerializerMixin):

    class Meta:
        model = FinanceUser
        fields = [
            "idx",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "dob",
            "father_name",
            "mother_name",
            "grandfather_name",
            "phone_number",
            "gender",
            "permanent_address",
            "temporary_address",
        ]




class PersonalGuarantorSerializer(BaseModelSerializerMixin):

    class Meta:
        model = PersonalGuarantor
        fields = ["idx", "user"]
        serializers = {
            "user": FinanceUserSerializer
        }

    
    def create(self, validated_data):
        loan_idx = self.context["loan_idx"]
        try:
            loan = LoanAccount.objects.get(idx=loan_idx)
        except LoanAccount.DoesNotExist:
            raise serializers.ValidationError("Loan does not exist")
        validated_data["loan"] = loan
        return super().create(validated_data)


       
class FinanceSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Finance
        fields = ["idx", "name", "parent", "email",  "description", "location", "phone_number", "website_url"]




class LoanAccountSerializer(BaseModelSerializerMixin):
    account_number = serializers.CharField(read_only=True)
    class Meta:
        model = LoanAccount
        fields = [
            "idx",
            "name",
            "user",
            "finance",
            "account_number",
            "loan_amount",
            "total_paid",
            "total_outstanding",
            "loan_limit",
            "interest_rate",
            "overdue_amount",
            "status",
            "loan_nature",
            "is_closed",
            "utilization_percent",
            "installment_due_type",
            "installment_amount",
            "utilization_percent",
            "maturity_date"
        ]
        serializers = {
            "user": FinanceUserSerializer,
            "finance": FinanceSerializer
        }

    def create(self, validated_data):
        account_number = generate_random_number(length=11)
        while LoanAccount.objects.filter(account_number=account_number).exists():
            account_number = generate_random_number(length=11)
        validated_data["account_number"] = account_number
        return super().create(validated_data)


class InstallmentSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Installment
        fields = [
            "idx",
            "loan",
            "due_date",
            "paid_date",
            "total_due",
            "total_paid",
            "total_outstanding",
        ]

        serializers = {
            "loan": LoanAccountSerializer
        }

class LoanApplicationSerializer(BaseModelSerializerMixin):
    user = FinanceUserSerializer()

    class Meta:
        model = LoanApplication
        fields = ["idx", "user", "finance", "loan_amount", "status"]

        serializers = {
            "user": FinanceUserSerializer,
            "finance": FinanceSerializer
        }


class CreateLoanApplicationSerializer(BaseModelSerializerMixin):
    user = FinanceUserSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True)
    middle_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    citizenship_number = serializers.CharField(write_only=True)
    citizenship_issued_place = serializers.CharField(write_only=True)
    citizenship_issued_date = serializers.DateField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    father_name = serializers.CharField(write_only=True)

    class Meta:
        model = LoanApplication
        fields = [
            "idx",
            "user",
            "finance",
            "first_name",
            "middle_name",
            "last_name",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "father_name",
            "phone_number",
            "loan_amount",
            "status",
        ]

        serializers = {
            "finance": FinanceSerializer
            
        }

    def create(self, validated_data):

        try:
            user = FinanceUser.objects.get(
                first_name=validated_data["first_name"],
                middle_name=validated_data["middle_name"],
                last_name=validated_data["last_name"],
            )
        except FinanceUser.DoesNotExist:
            user_data = {
                "first_name": validated_data["first_name"],
                "middle_name": validated_data["middle_name"],
                "last_name": validated_data["last_name"],
                "citizenship_number": validated_data["citizenship_number"],
                "citizenship_issued_place": validated_data["citizenship_issued_place"],
                "citizenship_issued_date": validated_data["citizenship_issued_date"],
                "phone_number": validated_data["phone_number"],
                "father_name": validated_data["father_name"],
                
            }
            user = FinanceUser.objects.create(**user_data)

        validated_data["user"] = user
        loan_application = LoanApplication.objects.create(
            finance=validated_data["finance"], user=user, loan_amount=validated_data["loan_amount"]
        )
        return loan_application


class UpdateLoanApplicationSerializer(BaseModelSerializerMixin):
    class Meta:
        model = LoanApplication
        fields = [
            "idx",
            "status",
        ]
        

class CompanySerializer(BaseModelSerializerMixin):
    class Meta:
        model = Company
        fields = [
            "idx",
            "name",
            "pan_num",
            "vat_num",
            "permanent_add",
            "pan_registration_date",
            "pan_registration_place",
            "profiter",
            "lone_taker_type",
        ]


class SecurityDepositSerializer(BaseModelSerializerMixin):
    class Meta:
        model = SecurityDeposit
        fields = [
            "idx",
            "loan",
            "type",
            "description",
            "ownership_type",
            "coverage_percentage",
            "nature_of_charge",
            "latest_value",
            "latest_valuation_date",
        ]
        serializers = {
            "loan": LoanAccountSerializer
        }


class BlacklistSerializer(BaseModelSerializerMixin):
     class Meta:
        model = Blacklist
        fields = [
            "idx",
            "user",
            "finance",
            "category",
            "reason",
            "remarks",
            "status",
            "release_date",
            "report_date",
        ]
        serializers = {
            "user": FinanceUserSerializer,
            "finance": FinanceSerializer
        }


class BlacklistReportSerializer(BaseModelSerializerMixin):
    class Meta:
        model = BlacklistReport
        fields = [
            "idx",
            "user",
            "finance",
            "status",
        ]
        serializers = {
            "user": FinanceUserSerializer,
            "finance": FinanceSerializer
        }


class FinanceStaffSerializer(BaseModelSerializerMixin):
    class Meta:
        model = FinanceStaff
        fields = [
            "idx",
            "user",
            "finance",
        ]
        serializers = {
            "user": UserSerializer,
            "finance": FinanceSerializer
        }


class InquirySerializer(BaseModelSerializerMixin):
 
    class Meta:
        model = Inquiry
        fields = [
            "idx",
            "user",
            "finance",
            "reason",
            "inquirer",
        ]
        serializers = {
            "user": FinanceUserSerializer,
            "finance": FinanceSerializer,
            "inquirer": FinanceStaffSerializer
        }
