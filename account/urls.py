from django.urls import path
from .views import fetch_xero_accounts,add_xero_account

urlpatterns = [
    path('fetch-accounts/', fetch_xero_accounts, name='fetch_xero_accounts'),
    path('add-accounts/', add_xero_account, name='add_xero_account'),
]
