from django.db import models

class XeroToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    id_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField()
