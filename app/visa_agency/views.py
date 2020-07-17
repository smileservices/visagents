from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import City, Service, AgencyService, VisaAgencyModel, Office
from .serializers import CitySerializer, ServiceSerializer, AgencyServiceSerializer, VisaAgencySerializer, \
    OfficeSerializer


@api_view()
def initial_data_view(request):
    #todo show only cities and services with agencies
    return Response({
        'cities': [CitySerializer(city).data for city in City.objects.all()],
        'services': [ServiceSerializer(service).data for service in Service.objects.all()],
    })


class AgencyView(viewsets.ModelViewSet):
    serializer_class = VisaAgencySerializer

    def get_queryset(self):
        return VisaAgencyModel.objects.all()


class AgencyServiceView(viewsets.ModelViewSet):
    serializer_class = AgencyServiceSerializer

    def get_queryset(self):
        queryset = AgencyService.objects.filter(service__id=self.kwargs['service_id'])
        if 'city_id' in self.kwargs and self.kwargs['city_id'] != 'all':
            queryset = queryset.filter(agency__office__city=self.kwargs['city_id'])
        return queryset.order_by('price').all()


'''
ADMIN
'''


class SuperAdminAgencyViewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = VisaAgencySerializer

    def get_queryset(self):
        return VisaAgencyModel.objects.all()


class SuperAdminOfficeViewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = OfficeSerializer

    def get_queryset(self):
        return Office.objects.all()


class SuperAdminAgencyServiceViewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = AgencyServiceSerializer

    def get_queryset(self):
        return AgencyService.objects.all()