from django.urls import path
from .views import fetch_xero_accounts,display_xero_accounts

urlpatterns = [
    path('fetch_xero_accounts/', fetch_xero_accounts, name='fetch_xero_accounts'),
    path('display_xero_accounts/', display_xero_accounts, name='display_xero_accounts'),
]
