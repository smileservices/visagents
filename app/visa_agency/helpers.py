from django.core.mail import EmailMessage
from .models import VisaAgencyModel, VisaAgencyProspect
from django.urls import reverse
from django.conf import settings
from django.template.loader import get_template


def count_city_agencies(city):
    count_agencies_registered = VisaAgencyModel.objects.filter(office__city=city).distinct().count()
    count_agencies_prospect = VisaAgencyProspect.objects.filter(city=city, unsubscribe=False).count()
    return count_agencies_registered + count_agencies_prospect


def send_quote_mails(quote_request):
    city = quote_request.expat.city
    expat = quote_request.expat
    prospect_list = VisaAgencyProspect.objects.filter(city=city, unsubscribe=False).all()
    # registered_list = VisaAgencyModel.objects.filter(office__city=city).distinct().all()
    mail_template = get_template('visa_agency/quote_mail.html')
    for agency in prospect_list:
        mail_body = mail_template.render(context={
            'agency': agency,
            'expat': expat,
            'quote_request': quote_request,
            'unsubscribe_url': settings.WEBSITE_URL + reverse('agency_unsubscribe') + '?uuid=' + agency.uuid.__str__()
        })
        prospect_email = EmailMessage(
            f'Request for {quote_request.service}',
            mail_body,
            'dontreply@visagents.com',
            [agency.email, ],
            reply_to=['mail@visagents.com'],
            headers={'Message-ID': 'Service Quote Request'},
        )
        prospect_email.send()
        agency.mails += 1
