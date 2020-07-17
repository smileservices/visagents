from rest_framework import routers
from .views import AgencyServiceView, initial_data_view, SuperAdminAgencyViewset, SuperAdminOfficeViewset, SuperAdminAgencyServiceViewset
from django.urls import path

router = routers.DefaultRouter()
# router.register('search/(?P<service_id>\d+)', AgencyServiceView, basename='agency-search-service')
router.register('search/(?P<service_id>\w+)/(?P<city_id>\w+)', AgencyServiceView, basename='agency-search-service-city')

# ADMIN
router.register('admin/agency', SuperAdminAgencyViewset, basename='super-admin-agency')
router.register('admin/office', SuperAdminOfficeViewset, basename='super-admin-office')
router.register('admin/agency-service', SuperAdminAgencyServiceViewset, basename='super-admin-agency-service')

urlpatterns = [
    path('initial-data/', initial_data_view)
]
urlpatterns += router.urls
