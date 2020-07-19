from django.urls import path, include
from rest_framework import routers
from django.contrib import admin

router = routers.DefaultRouter()

# Registration & Login
urlpatterns = [
    path('', include('frontend.urls')),
    path('superadmin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
]

urlpatterns += router.urls