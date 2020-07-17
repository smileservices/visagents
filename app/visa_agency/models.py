from django.db import models
from django.conf import settings
from core.models import City, Service
from subscription.models import Subscription
import uuid


class VisaAgencyProspect(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    unsubscribe = models.BooleanField(default=False)
    mails = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.mails} mails | {self.city} | {self.email} | {self.unsubscribe}'


class VisaAgencyModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(db_index=True, auto_now_add=True)
    active = models.BooleanField(default=True)
    description = models.TextField()
    website_url = models.TextField(null=True, blank=True)
    facebook = models.TextField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class AgencyUserNoteModel(models.Model):
    agency = models.ForeignKey(
        VisaAgencyModel, blank=True, null=True, on_delete=models.SET_NULL, related_name='notes'
    )
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    content = models.TextField()
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ("date",)


class Office(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    agency = models.ForeignKey(VisaAgencyModel, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.TextField(default='')
    geo_lat = models.TextField(null=True, blank=True)
    geo_lon = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.agency}-{self.city}'


class AgencyService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    agency = models.ForeignKey(VisaAgencyModel, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.agency}-{self.service}'
