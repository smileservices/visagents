from django.db import models
from django_countries.fields import CountryField


class City(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
