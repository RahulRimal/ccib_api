import pandas as pd

from django.db import transaction

from logging import Logger

from .models import Finance, FinanceUser, Installment, LoanAccount, LoanApplication
logger = Logger(__name__)


def import_finance_from_excel(file):
    try:
        df = pd.read_excel(file)
        # Converting headers to lowercase and replace spaces with underscores
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        logger.error(f"Excel: Error loading Excel file: {e}")
        return False

    finances = []
    for _, row in df.iterrows():
        finance = Finance(
            name=row.get('name'),
            description=row.get('description'),
            location=row.get('location'),
            email=row.get('email'),
            phone_number=row.get('phone_number'),
            website_url=row.get('website_url'),
        )
        finances.append(finance)

    try:
        Finance.objects.bulk_create(finances)
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Excel: Error importing finances: {e}")
        return False

    return True


def import_finance_user_from_excel(file):

    try:
        df = pd.read_excel(file)
        # Converting headers to lowercase and replace spaces with underscores
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        logger.error(f"Excel: Error loading Excel file: {e}")
        return False

    users = []
    for _, row in df.iterrows():
        user = FinanceUser(
            first_name=row.get('first_name'),
            middle_name=row.get('middle_name'),
            last_name=row.get('last_name'),
            email=row.get('email'),
            citizenship_number=row.get('citizenship_number'),
            citizenship_issued_place=row.get('citizenship_issued_place'),
            citizenship_issued_date=row.get('citizenship_issued_date'),
            gender=row.get('gender'),
            dob=row.get('dob'),
            father_name=row.get('father_name'),
            mother_name=row.get('mother_name'),
            grandfather_name=row.get('grandfather_name'),
            phone_number=row.get('phone_number'),
            permanent_address=row.get('permanent_address'),
            temporary_address=row.get('temporary_address'),
        )
        users.append(user)

    try:
        FinanceUser.objects.bulk_create(users)
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Excel: Error importing finance users: {e}")
        return False

    return True


@transaction.atomic
def import_loan_applications_from_excel(file, finance: Finance):
    try:
        df = pd.read_excel(file)
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        logger.error(f"Excel: Error loading Excel file: {e}")
        return False

    loan_applications = []
    for _, row in df.iterrows():
        user, created = FinanceUser.objects.get_or_create(
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            citizenship_number= row.get("citizenship_number"),
            citizenship_issued_place= row.get("citizenship_issued_place"),
            citizenship_issued_date= row.get("citizenship_issued_date"),
            email=row.get("email"),
            defaults={
                "middle_name": row.get("middle_name"),
                "gender": row.get("gender"),
                "dob": row.get("dob"),
                "father_name": row.get("father_name"),
                "mother_name": row.get("mother_name"),
                "grandfather_name": row.get("grandfather_name"),
                "phone_number": row.get("phone_number"),
                "permanent_address": row.get("permanent_address"),
                "temporary_address": row.get("temporary_address"),
            },
        )
        if created:
            print(f"Finance user created: {user.first_name} {user.last_name}")
            logger.info(f"Excel: Finance user created: {user.first_name} {user.last_name}")

        loan_application = LoanApplication(
            user=user,
            loan_amount=row.get("loan_amount"),
            finance=finance,
            status=row.get("status", LoanApplication.STATUS_PENDING),
        )
        loan_applications.append(loan_application)

    try:
        LoanApplication.objects.bulk_create(loan_applications)
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Excel: Error importing loan applications: {e}")
        return False

    return True


def import_loan_accounts_from_excel(file, finance: Finance):
    try:
        df = pd.read_excel(file)
        # Converting headers to lowercase and replacing spaces with underscores
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        logger.error(f"Excel: Error loading Excel file: {e}")
        return False

    loan_accounts = []
    for _, row in df.iterrows():

        loan_account = LoanAccount(
            finance=finance,
            name=row.get("name"),
            account_number=row.get("account_number"),
            installment_due_type=row.get(
                "installment_due_type", LoanAccount.INSTALLMENT_DUE_TYPE_DAILY
            ),
            total_paid=row.get("total_paid", 0.00),
            overdue_amount=row.get("overdue_amount", 0.00),
            status=row.get("status", LoanAccount.STATUS_GOOD),
            loan_nature=row.get("loan_nature", LoanAccount.NATURE_TERM),
            is_closed=row.get("is_closed", False),
            utilization_percent=row.get("utilization_percent"),
            maturity_date=row.get("maturity_date"),
            total_outstanding=row.get("total_outstanding", 0.00),
        )
        loan_accounts.append(loan_account)

    try:
        LoanAccount.objects.bulk_create(loan_accounts)
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Excel: Error importing loan accounts: {e}")
        return False

    return True


def import_installments_from_excel(file, loan_account: LoanAccount):
    try:
        df = pd.read_excel(file)
        # Converting headers to lowercase and replacing spaces with underscores
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        logger.error(f"Excel: Error loading Excel file: {e}")
        return False

    installments = []
    for _, row in df.iterrows():
        installment = Installment(
            loan=loan_account,
            due_date=row.get("due_date"),
            paid_date=row.get("paid_date"),
            total_due=row.get("total_due"),
            total_paid=row.get("total_paid"),
            total_outstanding=row.get("total_outstanding"),
        )
        installments.append(installment)

    try:
        Installment.objects.bulk_create(installments)
    except Exception as e:
        print(f"Error saving data: {e}")
        logger.error(f"Excel: Error importing installments: {e}")
        return False

    return True
