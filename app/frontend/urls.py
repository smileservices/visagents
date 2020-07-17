from django.urls import include, path
from frontend import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('data/', include('core.urls')),
    path('quote', views.quote_request, name='quote-request'),
    path('confirm-request', views.confirm_quote_request, name='confirm-quote-request'),
    path('unsubscribe/expat', views.expat_unsubscribe, name='expat_unsubscribe'),
    path('unsubscribe/agency', views.agency_unsubscribe, name='agency_unsubscribe'),
    path('admin/approve', views.admin_confirm_quote_request, name='admin_approve'),
]
