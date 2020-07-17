from django.contrib import admin
from .models import ExpatModel, VisaModel, VisaQuoteRequestModel

admin.site.register(ExpatModel)
admin.site.register(VisaModel)
admin.site.register(VisaQuoteRequestModel)

