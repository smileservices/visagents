from django.urls import path
from .views import get_city_list, get_service_list,get_country_list

urlpatterns = [
    path('countries', get_country_list, name='country-list'),
    path('cities', get_city_list, name='city-list'),
    path('services', get_service_list, name='service-list')
]
