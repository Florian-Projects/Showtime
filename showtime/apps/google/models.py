from django.db import models
from django.forms.models import model_to_dict


class GoogleAuthToken(models.Model):
    token = models.CharField(max_length=1024, null=False, blank=False)
    refresh_token = models.CharField(max_length=1024, null=False, blank=False)
    token_uri = models.CharField(max_length=1024, null=False, blank=False)
    client_id = models.CharField(max_length=1024, null=False, blank=False)
    client_secret = models.CharField(max_length=1024, null=False, blank=False)
    expiry = models.DateTimeField()

    @property
    def as_dict(self):
        model_dict = model_to_dict(self)
        model_dict["scope"] = ["https://www.googleapis.com/auth/calendar"]
        model_dict["expiry"] = model_dict["expiry"].strftime("%Y-%m-%dT%H:%M:%S")
        return model_dict
