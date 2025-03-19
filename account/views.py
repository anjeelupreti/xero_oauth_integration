from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.conf import settings
import datetime
import requests

import logging

logger = logging.getLogger(__name__)

from oauth.models import XeroToken
from oauth.views import check_and_refresh_token
from .models import XeroAccount

def get_xero_tenant_id():
    """Fetch and return the Xero Tenant ID."""
    check_and_refresh_token() 
    token = XeroToken.objects.first()
    
    # Check if the token exists and is valid
    if not token or not token.access_token:
        logger.error("No valid XeroToken found or token is invalid.")
        logger.error("No valid XeroToken found or token is invalid.")
        return None  
    
    headers = {"Authorization": f"Bearer {token.access_token}"}
    # Corrected URL concatenation
    xero_tenant_id_url = settings.XERO_TENANT_ID_URL
    response = requests.get(f"{xero_tenant_id_url}", headers=headers)

    if response.status_code == 200:
        tenants = response.json()
        if tenants and isinstance(tenants, list) and len(tenants) > 0:
            logger.error(f'Total tenants: {tenants}')
            
            tenant_id = tenants[0]['tenantId']
            for tenant in tenants:
                if tenant.get("tenantName") == "Demo Company (Global)":  # Match by tenant name
                    tenant_id = tenant.get("id")  # If match found, get tenantId
                    break  # Exit loop after finding the correct tenant
            
            if tenant_id:
                logger.info(f"Retrieved Tenant ID for : {tenant_id}")
                logger.error(f"Retrieved Tenant ID t: {tenant_id}")
                return tenant_id
            else:
                logger.error("Tenant  not found in the API response.")
                return None
    
    logger.error(f"Failed to get Tenant ID. Response: {response.text}")
    logger.error(f"Failed to get Tenant ID. Response: {response.text}")  
    return None 



def fetch_xero_accounts(request):
    """Fetch Xero accounts from API and store them in the database."""
    
    tenant_id = get_xero_tenant_id()
    if not tenant_id:
        return render(request, "account/account_chart.html", {"error": "No valid Tenant ID found."})
    
    token = XeroToken.objects.first()
    if not token or not token.access_token:
        return render(request, "account/account_chart.html", {"error": "No valid access token."})
    
    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "xero-tenant-id": tenant_id,
        "Accept": "application/json"
    }
    xero_account_url = settings.XERO_ACCOUNT_URL
    response = requests.get(xero_account_url, headers=headers)
    logger.error('Account URL Validated    ----------------------------->')
    
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
                        # "description": acc.get("Description"),
                        # "tax_type": acc.get("TaxType"),
                        # "bank_account_number": acc.get("BankAccountNumber"),
                        # "bank_account_type": acc.get("BankAccountType"),
                        # "currency_code": acc.get("CurrencyCode"),
                        # "enable_payments": acc.get("EnablePaymentsToAccount", False),
                        # "show_in_expense_claims": acc.get("ShowInExpenseClaims", False),
                        # "status": acc.get("Status"),
                        # "account_class": acc.get("Class"),
                        # "system_account": acc.get("SystemAccount", False), 
                        # "reporting_code": acc.get("ReportingCode"),
                        # "reporting_code_name": acc.get("ReportingCodeName"),
                        # "has_attachments": acc.get("HasAttachments", False),
                        # "add_to_watchlist": acc.get("AddToWatchlist", False),
                        # "updated_date_utc": make_aware(datetime.datetime.strptime(
                        #     acc.get("UpdatedDateUTC"), "%Y-%m-%dT%H:%M:%SZ"
                        # )) if acc.get("UpdatedDateUTC") else None
                    }
                )
            saved_accounts = XeroAccount.objects.all()
            print(saved_accounts)
            return render(request, "account/account_chart.html", {"accounts": saved_accounts})
        
        except (ValueError, KeyError, TypeError) as e:
            logger.error(f"Error parsing Xero API response: {str(e)}")
            return render(request, "account/account_chart.html", {"error": "Failed to parse Xero API response."})
    
    # Log the response if the status code is not 200
    logger.error(f"Error fetching accounts: {response.text}")
    return render(request, "account/account_chart.html", {"error": f"Error fetching accounts: {response.text}"})

def display_xero_accounts(request):
    """Retrieve stored Xero accounts and display them."""
    accounts = XeroAccount.objects.all()
    return render(request, "account/account_chart.html", {"accounts": accounts})
