from django.http import JsonResponse
from json import dumps
from core.models import City, Service
from django_countries import countries


def get_city_list(request):
    return JsonResponse(data=[{'value': c.pk, 'label': c.name} for c in City.objects.all()], safe=False)


def get_service_list(request):
    return JsonResponse(data=[{'value': s.pk, 'label': s.name} for s in Service.objects.all()], safe=False)


def get_country_list(request):
    return JsonResponse(data=[{'value': idx, 'label': c} for idx, c in countries.countries.items()], safe=False)

