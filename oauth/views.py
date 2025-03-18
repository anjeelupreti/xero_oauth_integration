import requests
import datetime
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone  # Import timezone for timezone-aware datetime
from .models import XeroToken
import secrets

def xero_login_page(request):
    return render(request, 'oauth/xero_login_page.html')

def redirect_to_xero(request):
    state = secrets.token_urlsafe(16)  
    xero_client_id = settings.XERO_CLIENT_ID
    xero_redirect_uri = settings.XERO_REDIRECT_URI
    
    auth_url = f"{settings.XERO_AUTH_URL}?response_type=code&client_id={xero_client_id}&redirect_uri={xero_redirect_uri}&scope=openid profile accounting.transactions&state={state}"
    request.session["xero_auth_state"] = state
    return redirect(auth_url)

def xero_callback(request):
    code = request.GET.get("code")
    if not code:
        return render(request, 'oauth/xero_callback.html', {"message": "Authorization failed", "access": False})

    returned_state = request.GET.get("state")
    stored_state = request.session.get("xero_auth_state")

    # if not returned_state or returned_state != stored_state:
    #     return render(request, 'oauth/xero_callback.html', {"message": "Invalid state parameter", "access": False})

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.XERO_REDIRECT_URI,
        "client_id": settings.XERO_CLIENT_ID,
        "client_secret": settings.XERO_CLIENT_SECRET,
    }

    response = requests.post(settings.XERO_TOKEN_URL, data=data)
    token_data = response.json()

    if "access_token" in token_data:
        # Make expires_at timezone-aware
        expires_at = timezone.now() + datetime.timedelta(seconds=token_data['expires_in'])
        XeroToken.objects.update_or_create(
            id=1,
            defaults={
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": expires_at,
            }
        )
        return render(request, 'oauth/xero_callback.html', {"message": "Token saved successfully", "access": True})

    return render(request, 'oauth/xero_callback.html', {"message": "Token exchange failed", "access": False})

def refresh_xero_token():
    token = XeroToken.objects.first()
    if not token or not token.refresh_token:
        return {"error": "No refresh token available"}

    data = {
        "grant_type": "refresh_token",
        "refresh_token": token.refresh_token,
        "client_id": settings.XERO_CLIENT_ID,
        "client_secret": settings.XERO_CLIENT_SECRET,
    }

    response = requests.post(settings.XERO_TOKEN_URL, data=data)
    token_data = response.json()

    if "access_token" in token_data:
        # Make expires_at timezone-aware
        expires_at = timezone.now() + datetime.timedelta(seconds=token_data['expires_in'])
        token.access_token = token_data['access_token']
        token.refresh_token = token_data['refresh_token']
        token.expires_at = expires_at
        token.save()
        return {"success": "Token refreshed"}
    return {"error": "Token refresh failed"}

def check_and_refresh_token():
    token = XeroToken.objects.first()
    if token and token.expires_at:
        # Use timezone.now() to get the current time (aware datetime)
        if timezone.now() >= token.expires_at:
            return refresh_xero_token()
    return {"status": "Token is valid"}

def refresh_token_view(request):
    result = refresh_xero_token()
    return JsonResponse(result)
