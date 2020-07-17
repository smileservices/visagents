from django.shortcuts import render
from django.core.mail import EmailMessage, mail_admins
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from json import loads, dumps
from expat.models import ExpatModel, VisaModel, VisaQuoteRequestModel
from datetime import datetime, timedelta
from core.models import City, Service
from visa_agency.models import VisaAgencyModel, VisaAgencyProspect
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import AllowAny
from django.urls import reverse
from visa_agency import helpers as agency_helpers
from django.conf import settings
from django.template.loader import get_template
from users.models import CustomUser


class SendQuoteRequestThrottle(UserRateThrottle):
    rate = '30/day'


class RegisterAgencyProspectThrottle(UserRateThrottle):
    rate = '10/day'


def homepage(request):
    return render(request, 'frontend/homepage.html')


def extract_values(d):
    try:
        if type(d) is list:
            return [e['value'] for e in d]
        elif type(d) is dict:
            return d['value']
        else:
            raise ValueError('Can extract values only from list or dict')
    except KeyError:
        raise KeyError('Must supply dictionary with value key')


@api_view(http_method_names=['POST'])
@throttle_classes([SendQuoteRequestThrottle])
@permission_classes([AllowAny])
def quote_request(request):
    data = request.data
    try:
        # check if expat with same email already exist
        city = City.objects.get(pk=extract_values(data['userData']['city']))
        expat = ExpatModel.objects.get(email=data['userData']['email'])
        expat.city = city
        expat.save()
        # only accept new request if older than 5 days
        expat.requests.get(date__gt=datetime.now() - timedelta(days=5))
        return Response({
            'hasError': True,
            'success': False,
            'text': 'We are limiting the quote requests to one every 5 days. There is already a quote requested posted by your email less than 5 days ago.'
        })
    except City.DoesNotExist:
        return Response({
            'hasError': True,
            'success': False,
            'text': 'Invalid city provided'
        })
    except ExpatModel.DoesNotExist:
        # if expat doesn't exist, create expat and its visa
        expat = ExpatModel(
            email=data['userData']['email'],
            phone=data['userData']['phone'],
            name=data['userData']['name'],
            nationality=extract_values(data['userData']['nationality']),
            city=city
        )
        expat.save()
        visa = VisaModel(
            expat=expat,
            type=data['visaData']['type'],
            issue_place=data['visaData']['issue_place'],
            issue_date=data['visaData']['issue_date'],
            expiration=data['visaData']['expiration'],
            entry_port=data['visaData']['entry_port'],
            entry_date=data['visaData']['entry_date'],
        )
        visa.save()
    except VisaQuoteRequestModel.DoesNotExist:
        # if visa quote is not found, get or create visa
        visa = VisaModel.objects.get_or_create(
            expat=expat,
            type=data['visaData']['type'],
            issue_place=data['visaData']['issue_place'],
            issue_date=data['visaData']['issue_date'],
            expiration=data['visaData']['expiration'],
            entry_port=data['visaData']['entry_port'],
            entry_date=data['visaData']['entry_date'],
        )
    service = Service.objects.get(pk=extract_values(data['serviceData']['service']))
    quote_request = VisaQuoteRequestModel(
        expat=expat,
        visa=visa,
        persons=data['serviceData']['persons'],
        service=service,
        note=data['serviceData']['note']
    )
    quote_request.save()
    count_agencies = agency_helpers.count_city_agencies(expat.city)
    confirm_mail_template = get_template('expat/confirm_request.html')
    mail_body = confirm_mail_template.render(context={
        'expat': expat,
        'confirm_url': settings.WEBSITE_URL + reverse(
            'confirm-quote-request') + '?request_uuid=' + quote_request.uuid.__str__(),
        'agencies_count': count_agencies
    })
    email = EmailMessage(
        'Confirm your visa service request',
        mail_body,
        'dontreply@visagents.com',
        [expat.email, ],
        reply_to=['vladimir.gorea@gmail.com'],
        headers={'Message-ID': 'confirmation of visa quote request'},
    )
    email.send()
    return Response({
        'hasError': False,
        'success': True,
        'text': f'Email containing confirmation link was sent to {expat.email}. Please click on the provided link to activate the request and to send it to {count_agencies} visa agents in {expat.city}'
    })


@api_view(http_method_names=['POST'])
@throttle_classes([RegisterAgencyProspectThrottle])
@permission_classes([AllowAny])
def register_visa_agency_prospect(request):
    data = request.data
    try:
        VisaAgencyProspect.objects.get(email=data['email'])
        return Response({
            'hasError': False,
            'success': True,
            'text': f'We already have you registered as an agency! If you are not receiving visa requests, please contact our support.'
        })
    except VisaAgencyProspect.DoesNotExist:
        pass
    city = City.objects.get(pk=extract_values(data['city']))
    prospect = VisaAgencyProspect(
        name=data['name'],
        email=data['email'],
        city=city,
        unsubscribe=True
    )
    prospect.save()
    mail_template = get_template('frontend/prospect_register_mail.html')
    mail_body = mail_template.render(context={
        'agency': prospect,
        'confirm_url': settings.WEBSITE_URL + reverse('prospect-confirm') + f'?uuid={prospect.uuid.__str__()}'
    })
    email = EmailMessage(
        'Confirm your email',
        mail_body,
        'dontreply@visagents.com',
        [prospect.email, ],
        reply_to=['vladimir.gorea@gmail.com'],
        headers={'Message-ID': 'confirmation of visa agency registration'},
    )
    email.send()
    return Response({
        'hasError': False,
        'success': True,
        'text': f'Email containing confirmation link was sent to {prospect.email}. Please click on the provided link to start receiving emails.'
    })


def send_quote_request_to_admin(quote_request):
    template = get_template('frontend/admin_quote_mail.html')
    admin_user = CustomUser.objects.get(is_staff=True)
    email_body = template.render(context={
        'quote_request': quote_request,
        'expat': quote_request.expat,
        'visa': quote_request.visa,
        'approve_url': settings.WEBSITE_URL + reverse(
            'admin_approve') + f'?adm_key={admin_user.uuid.__str__()}&req_key={quote_request.uuid.__str__()}'
    })

    mail_admins(
        'New visa quote request',
        email_body
    )


def confirm_prospect_email(request):
    prospect_uuid = request.GET.get('uuid')
    data = {
        'status': 'Could not confirm :(',
        'message': 'The provided link is missing request key.'
    }
    if prospect_uuid:
        try:
            prospect = VisaAgencyProspect.objects.get(uuid=prospect_uuid)
            prospect.unsubscribe = False
            prospect.save()
            data['status'] = 'Success!'
            data['message'] = f'Your visa agency was successfully registered'
            mail_admins(
                'new prospect registered',
                f'Prospect {prospect.name} from {prospect.city} registered',
            )
        except VisaAgencyProspect.DoesNotExist:
            data['status'] = 'Could not confirm :('
            data['message'] = 'Confirm request is not valid!'
        except ValidationError:
            data['status'] = 'Could not confirm :('
            data['message'] = 'Confirm request is not valid!'
    return render(request, 'frontend/withmessage.html', data)


def admin_confirm_quote_request(request):
    request_uuid = request.GET['req_key']
    admin_uuid = request.GET['adm_key']
    data = {
        'status': 'Could not confirm :(',
        'message': 'The provided link is missing request key.'
    }
    try:
        CustomUser.objects.get(uuid=admin_uuid, is_staff=True)
        quote_request = VisaQuoteRequestModel.objects.get(uuid=request_uuid)
        agency_helpers.send_quote_mails(quote_request)
        data = {
            'status': 'Emails sent',
            'message': 'All good'
        }
    except CustomUser.DoesNotExist:
        data = {
            'status': 'Forbidden',
            'message': 'You are forbidden to take this action'
        }
    except VisaQuoteRequestModel.DoesNotExist:
        data = {
            'status': 'Can\'t Find Quote Request',
            'message': 'Could not find the quote request'
        }
    except ValidationError:
        data['status'] = 'Could not confirm :('
        data['message'] = 'Confirm request is not valid!'
    return render(request, 'frontend/withmessage.html', data)


def confirm_quote_request(request):
    expat_uuid = request.GET.get('request_uuid')
    data = {
        'status': 'Could not confirm :(',
        'message': 'The provided link is missing request key.'
    }
    if expat_uuid:
        try:
            quote_request = VisaQuoteRequestModel.objects.get(uuid=expat_uuid)
            quote_request.active = True
            quote_request.save()
            data['status'] = 'Success!'
            data[
                'message'] = f'Your visa quote request has been validated and will be sent to visa agencies in {quote_request.expat.city}'
            send_quote_request_to_admin(quote_request)
        except VisaQuoteRequestModel.DoesNotExist:
            data['status'] = 'Could not confirm :('
            data['message'] = 'Confirm request is not valid!'
        except ValidationError:
            data['status'] = 'Could not confirm :('
            data['message'] = 'Confirm request is not valid!'
    return render(request, 'frontend/withmessage.html', data)


def expat_unsubscribe(request):
    uuid = request.GET.get('uuid')
    data = {
        'status': 'Bad link :(',
        'message': 'The provided link is missing your key.'
    }
    if uuid:
        try:
            expat = ExpatModel.objects.get(uuid=uuid)
            expat.subscribed = False
            expat.save()
            data['status'] = 'Unsubscribed :('
            data['message'] = 'You\'ve been successfully unsubscribed'
        except ExpatModel.DoesNotExist:
            data['status'] = 'We\'re sorry :('
            data['message'] = 'Could not find your details on our server'
        except ValidationError:
            data['status'] = 'We\'re sorry :('
            data['message'] = 'Unsubscribed request is did not validate!'
    return render(request, 'frontend/withmessage.html', data)


def agency_unsubscribe(request):
    uuid = request.GET.get('uuid')
    data = {
        'status': 'Bad link :(',
        'message': 'The provided link is missing your key.'
    }
    if uuid:
        try:
            agency = VisaAgencyProspect.objects.get(uuid=uuid)
            agency.unsubscribe = True
            agency.save()
            data['status'] = 'Unsubscribed :('
            data['message'] = 'You\'ve been successfully unsubscribed'
            mail_admins(
                f'{agency} unsubscribed',
                f'{agency} just unsubscribed'
            )
        except ExpatModel.DoesNotExist:
            data['status'] = 'We\'re sorry :('
            data['message'] = 'Could not find your details on our server'
        except ValidationError:
            data['status'] = 'We\'re sorry :('
            data['message'] = 'Unsubscribed request is did not validate!'
    return render(request, 'frontend/withmessage.html', data)
