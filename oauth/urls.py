from django.urls import path
from .views import redirect_to_xero, xero_callback, refresh_token_view , xero_login_page

urlpatterns = [
    path('xero-login/',xero_login_page, name='xero_login_page'),
    path('redirect-xero/',redirect_to_xero, name='redirect_to_xero'),
    # path('callback/', xero_callback, name='xero_callback'),
    path('refresh-token/', refresh_token_view, name='refresh_token'),
]
