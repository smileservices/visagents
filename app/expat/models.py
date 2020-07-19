from django.db import models
from django_countries.fields import CountryField
from django.conf import settings
from core.models import Service, City
from visa_agency.models import VisaAgencyModel
import uuid


class ExpatModel(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    subscribed = models.BooleanField(default=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True, null=True
    )
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    nationality = CountryField(multiple=True)

    def nationality_str(self):
        return ', '.join([n.name for n in self.nationality])

    def __str__(self):
        return f'{self.name} | {self.nationality_str()}'


class VisaModel(models.Model):
    expat = models.ForeignKey(ExpatModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    issue_place = models.CharField(max_length=128)
    issue_date = models.DateField()
    expiration = models.DateField()
    entry_date = models.DateField()
    entry_port = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.expat} | visa type: {self.type} | expire: {self.expiration}'


class VisaQuoteRequestModel(models.Model):
    active = models.BooleanField(default=False)
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    expat = models.ForeignKey(ExpatModel, on_delete=models.CASCADE, blank=True, null=True, related_name='requests')
    date = models.DateTimeField(auto_now_add=True)
    persons = models.IntegerField(default=1)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    note = models.TextField()
    visa = models.ForeignKey(VisaModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.visa} | service: {self.service} | {self.date}'


class VisaQuoteResponseModel(models.Model):
    agent = models.ForeignKey(VisaAgencyModel, on_delete=models.CASCADE)
    request = models.ForeignKey(VisaQuoteRequestModel, on_delete=models.CASCADE)
    price = models.FloatField(help_text='Price in USD')
    duration = models.IntegerField(help_text='How many days it will take')
    note = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
