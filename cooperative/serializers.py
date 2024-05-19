from rest_framework import serializers

from autho.models import User
from autho.serializers import UserSerializer
from common.helpers import generate_username
from common.mixins import BaseModelSerializerMixin
from cooperative.models import (
    Company,
    Finance,
    Loan,
    LoanApplication,
    PersonalGuarantor,
)


class PersonalGuarantorSerializer(BaseModelSerializerMixin):
    user = UserSerializer()

    class Meta:
        model = PersonalGuarantor
        fields = ["idx", "user"]


class CreatePersonalGuarantorSerializer(BaseModelSerializerMixin):
    user_idx = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = PersonalGuarantor
        fields = ["idx", "user_idx", "user"]

    def create(self, validated_data):
        loan_idx = self.context["loan_idx"]
        try:
            user = User.objects.get(idx=validated_data.pop("user_idx"))
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        try:
            loan = Loan.objects.get(idx=loan_idx)
        except Loan.DoesNotExist:
            raise serializers.ValidationError("Loan does not exist")
        validated_data["loan"] = loan
        return super().create(validated_data)

        # def create(self, validated_data):
        #     try:
        #         user = User.objects.get(
        #             first_name=validated_data["first_name"],
        #             middle_name=validated_data["middle_name"],
        #             last_name=validated_data["last_name"],
        #         )
        #     except User.DoesNotExist:
        #         data = validated_data
        #         data.pop("user")
        #         data["username"] = generate_username(
        #             validated_data["first_name"], validated_data["last_name"]
        #         )
        #         user = User.objects.create(**data)

        #     validated_data["user"] = user
        #     PersonalGuarantor = PersonalGuarantor.objects.create(
        #         user=user, **validated_data["user"]    first_name = serializers.CharField(write_only=True)

        #     )
        #     return PersonalGuarantor


class FinanceSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Finance
        fields = ["idx", "name", "description", "location"]


class LoanSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Loan
        fields = [
            "idx",
            "name",
            "nature",
            "amount",
            "maturity_date",
            "installment_due_type",
            "emi_amount",
            "currently_outstanding",
            "total_due",
            "personal_guarantors",
        ]


class CreateLoanSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Loan
        fields = [
            "idx",
            "name",
            "nature",
            "amount",
            "maturity_date",
            "installment_due_type",
            "emi_amount",
            "currently_outstanding",
            "total_due",
        ]


class UpdateLoanSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Loan
        fields = [
            "idx",
            "name",
            "nature",
            "amount",
            "maturity_date",
            "installment_due_type",
            "emi_amount",
            "currently_outstanding",
            "total_due",
        ]


class LoanApplicationSerializer(BaseModelSerializerMixin):
    user = UserSerializer()
    finance = FinanceSerializer()
    finance_idx = serializers.CharField(write_only=True)

    class Meta:
        model = LoanApplication
        fields = ["idx", "user", "finance", "loan_amount", "status", "finance_idx"]

    def create(self, validated_data):
        try:
            finance = Finance.objects.get(idx=validated_data.pop("finance_idx"))
        except Finance.DoesNotExist:
            raise serializers.ValidationError("Finance does not exist")
        validated_data["finance"] = finance
        try:
            user = User.objects.get(
                first_name=validated_data["first_name"],
                middle_name=validated_data["middle_name"],
                last_name=validated_data["last_name"],
            )
        except User.DoesNotExist:
            data = validated_data
            data.pop("loan_amount")
            data["username"] = generate_username(
                validated_data["first_name"], validated_data["last_name"]
            )
            user = User.objects.create(**data)

        validated_data["user"] = user
        loan_application = LoanApplication.objects.create(
            finance=finance, user=user, loan_amount=validated_data["loan_amount"]
        )
        return loan_application


class CreateLoanApplicationSerializer(BaseModelSerializerMixin):
    user = UserSerializer(read_only=True)
    finance = FinanceSerializer(read_only=True)
    finance_idx = serializers.CharField(write_only=True)
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
            "finance_idx",
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

    def create(self, validated_data):
        try:
            finance = Finance.objects.get(idx=validated_data.pop("finance_idx"))
        except Finance.DoesNotExist:
            raise serializers.ValidationError("Finance does not exist")
        validated_data["finance"] = finance

        try:
            user = User.objects.get(
                first_name=validated_data["first_name"],
                middle_name=validated_data["middle_name"],
                last_name=validated_data["last_name"],
            )
        except User.DoesNotExist:
            data = validated_data
            data.pop("loan_amount")
            data["username"] = generate_username(
                validated_data["first_name"], validated_data["last_name"]
            )
            user = User.objects.create(**data)

        validated_data["user"] = user
        loan_application = LoanApplication.objects.create(
            finance=finance, user=user, loan_amount=validated_data["loan_amount"]
        )
        return loan_application


class UpdateLoanApplicationSerializer(BaseModelSerializerMixin):
    class Meta:
        model = LoanApplication
        fields = [
            "idx",
            "status",
        ]

    # def update(self,instance, validated_data):
    #     try:
    #         finance = Finance.objects.get(idx=validated_data.pop("finance_idx"))
    #     except Finance.DoesNotExist:
    #         raise serializers.ValidationError("Finance does not exist")
    #     validated_data["finance"] = finance

    #     try:
    #         user = User.objects.get(
    #             first_name=validated_data["first_name"],
    #             middle_name=validated_data["middle_name"],
    #             last_name=validated_data["last_name"],
    #         )
    #     except User.DoesNotExist:
    #         data = validated_data
    #         data.pop("loan_amount")
    #         data["username"] = generate_username(
    #             validated_data["first_name"], validated_data["last_name"]
    #         )
    #         user = User.objects.update(**data)

    #     validated_data["user"] = user
    #     loan_application = LoanApplication.objects.update(
    #         finance=finance,user=user, loan_amount=validated_data["loan_amount"]
    #     )
    #     return loan_application


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


class CreateCompanySerializer(BaseModelSerializerMixin):
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


class UpdateCompanySerializer(BaseModelSerializerMixin):
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
            "share_holders",
            "profiter",
            "lone_taker_type",
        ]
