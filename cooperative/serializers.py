from rest_framework import serializers

from finance_cbi.cib.models import Loan, PersonalGuarantor, Company


class PersonalGuarantorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalGuarantor
        fields = [
            "id",
            "name",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "dob",
            "father_name",
        ]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "name",
            "nature",
            "amount",
            "disbursed_date",
            "maturity_date",
            "installment_due_type",
            "emi",
            "currently_outstanding",
            "total_due",
            "personal_guarantors",
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "pan_num",
            "vat_num",
            "permanent_add",
            "pan_registration_date",
            "pan_registration_place",
            "share_holders",
            "if_profiter_then_no_shareholders",
            "profiter",
            "loan_taker_type",
        ]
