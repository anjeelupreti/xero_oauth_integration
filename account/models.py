from django.db import models

class XeroAccount(models.Model):
    account_id = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    tax_type = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=100, null=True, blank=True)
    bank_account_type = models.CharField(max_length=50, null=True, blank=True)
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    enable_payments = models.BooleanField(default=False)
    updated_date_utc = models.DateTimeField(auto_now=True)
