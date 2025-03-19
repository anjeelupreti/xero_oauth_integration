from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.conf import settings
import datetime
import requests

from oauth.models import XeroToken
from oauth.views import check_and_refresh_token
from .models import XeroAccount

def fetch_xero_accounts(request):
    """Fetch Xero accounts from API and store them in the database."""
    check_and_refresh_token()  
    token = XeroToken.objects.first()
    
    if not token:
        return render(request, "account/account_chart.html", {"error": "No valid access token."})
    
    headers = {"Authorization": f"Bearer {token.access_token}"}
    response = requests.get(settings.XERO_ACCOUNT_URL, headers=headers)
    
    if response.status_code == 200:
        try:
            accounts_data = response.json()
            accounts = accounts_data.get("Accounts", [])
            
            for acc in accounts:
                XeroAccount.objects.update_or_create(
                    account_id=acc.get("AccountID"),
                    defaults={
                        "code": acc.get("Code"),
                        "name": acc.get("Name"),
                        "type": acc.get("Type"),
                        "description": acc.get("Description"),
                        "tax_type": acc.get("TaxType"),
                        "bank_account_number": acc.get("BankAccountNumber"),
                        "bank_account_type": acc.get("BankAccountType"),
                        "currency_code": acc.get("CurrencyCode"),
                        "enable_payments": acc.get("EnablePaymentsToAccount", False),
                        "show_in_expense_claims": acc.get("ShowInExpenseClaims", False),
                        "status": acc.get("Status"),
                        "account_class": acc.get("Class"),
                        "system_account": acc.get("SystemAccount"),
                        "reporting_code": acc.get("ReportingCode"),
                        "reporting_code_name": acc.get("ReportingCodeName"),
                        "has_attachments": acc.get("HasAttachments", False),
                        "add_to_watchlist": acc.get("AddToWatchlist", False),
                        "updated_date_utc": make_aware(datetime.datetime.strptime(
                            acc.get("UpdatedDateUTC"), "%Y-%m-%dT%H:%M:%SZ"
                        )) if acc.get("UpdatedDateUTC") else None
                    }
                )
            
            return redirect("display_xero_accounts")
        except ValueError:
            return render(request, "account/account_chart.html", {"error": "Failed to parse Xero API response."})
    
    return render(request, "account/account_chart.html", {"error": f"Error fetching accounts: {response.text}"})

def display_xero_accounts(request):
    """Retrieve stored Xero accounts and display them."""
    accounts = XeroAccount.objects.all()
    return render(request, "account/account_chart.html", {"accounts": accounts})
