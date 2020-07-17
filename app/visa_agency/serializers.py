from rest_framework.serializers import ModelSerializer
from .models import City, Service, AgencyService, VisaAgencyModel, Office


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']


class OfficeSerializer(ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Office
        fields = ['id', 'city', 'agency', 'address', 'contact']

    def run_validation(self, data):
        validated = {
            'city': City.objects.get(pk=data['city']),
            'address': data['address'],
            'contact': data['contact'],
        }
        if 'agency_id' in data:
            validated['agency_id'] = data['agency_id']
        return validated


class ShortAgencySerializer(ModelSerializer):
    class Meta:
        model = VisaAgencyModel
        fields = ['id', 'name']


class AgencyServiceShortSerializer(ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = AgencyService
        fields = ['id', 'service', 'price']


class VisaAgencySerializer(ModelSerializer):
    office_set = OfficeSerializer(many=True, required=False)
    agencyservice_set = AgencyServiceShortSerializer(many=True, required=False)

    class Meta:
        model = VisaAgencyModel
        fields = ['id', 'name', 'description', 'website_url', 'facebook', 'office_set', 'agencyservice_set']


class AgencyServiceSerializer(ModelSerializer):
    service = ServiceSerializer()
    agency = VisaAgencySerializer()

    class Meta:
        model = AgencyService
        fields = ['id', 'service', 'agency', 'price']

    def run_validation(self, data):
        validated = {
            'service': Service.objects.get(pk=data['service']),
            'price': data['price']
        }
        if 'agency_id' in data:
            validated['agency_id'] = data['agency_id']
        return validated
