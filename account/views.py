from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
import datetime
from oauth.models import XeroToken
from oauth.views import check_and_refresh_token
from .models import XeroAccount

def fetch_xero_accounts(request):
    check_and_refresh_token()  # Ensure valid token

    token = XeroToken.objects.first()
    if not token:
        return render(request, "account/account_chart.html", {"error": "No valid access token"})

    print(f"Access Token: {token.access_token}")  # Log the access token

    headers = {"Authorization": f"Bearer {token.access_token}"}
    xero_account_url = settings.XERO_ACCOUNT_URL

    response = requests.get(xero_account_url, headers=headers)


    try:
        accounts_data = response.json()
        if "Accounts" not in accounts_data:
            return render(request, "account/account_chart.html", {"error": "Accounts data missing from API response."})

        accounts = accounts_data.get("Accounts", [])
        if accounts:
            formatted_accounts = []
            for acc in accounts:
                account = {
                    "AccountID": acc.get("AccountID"),
                    "Code": acc.get("Code"),
                    "Name": acc.get("Name"),
                    "Type": acc.get("Type")
                }
                formatted_accounts.append(account)

            # Passing the formatted accounts to the template
            return render(request, "account/account_chart.html", {"accounts": formatted_accounts})
        else:
            return render(request, "account/account_chart.html", {"error": "No accounts found in the response"})

    except ValueError:
        return render(request, "account/account_chart.html", {"error": "Failed to parse the response from Xero API"})


def add_xero_account(request):
    if request.method == "POST":
        account_code = request.POST.get("account_code")
        account_name = request.POST.get("account_name")
        account_type = request.POST.get("account_type")
        
        if not account_code or not account_name or not account_type:
            return render(request, "account/add_account.html", {"error": "All fields are required"})

        account_data = {
            "Code": account_code,
            "Name": account_name,
            "Type": account_type
        }

        print(f"Account Data: {account_data}")  

        check_and_refresh_token() 
        token = XeroToken.objects.first()

        if not token:
            return render(request, "account/add_account.html", {"error": "No valid access token"})

        print(f"Access Token: {token.access_token}") 

        headers = {"Authorization": f"Bearer {token.access_token}"}
        xero_account_url = settings.XERO_ACCOUNT_URL
        
        response = requests.post(xero_account_url, json={"Accounts": [account_data]}, headers=headers)

        print(f"Response Status Code: {response.status_code}") 
        print(f"Response Content: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            if "Accounts" in response_data:
                return render(request, "account/add_account.html", {"message": "Account added successfully"})
            else:
                return render(request, "account/add_account.html", {"error": "Failed to create the account in Xero"})
        else:
            return render(request, "account/add_account.html", {"error": f"Failed to create account. Error: {response.text}"})

    return render(request, "account/add_account.html")
