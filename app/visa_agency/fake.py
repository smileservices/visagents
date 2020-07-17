from random import choice, choices, randint
from faker import Faker
from .models import VisaAgencyProspect, VisaAgencyModel, AgencyService, Office
from core.models import City, Service
from users.fake import create_user
from subscription.models import SubscriptionType, Subscription, SUBSTATUS
from datetime import datetime, date
f = Faker()


def create_visa_agency_prospect():
    vap = VisaAgencyProspect(
        name=f.company(),
        email=f.email(),
        city=choice(City.objects.all())
    )
    vap.save()


def create_visa_agency():
    user = create_user()
    free_subscription = SubscriptionType.objects.get(idx='freeleads')
    subscription = Subscription(
        type=free_subscription,
        leads=free_subscription.leads,
        status=SUBSTATUS.ACTIVE
    )
    subscription.save()
    visa_agency = VisaAgencyModel(
        user=user,
        name=f.company(),
        description=f.text(),
        website_url=f.url(),
        facebook=f.url(),
        subscription=subscription
    )
    visa_agency.save()
    services = choices(Service.objects.all(), k=3)
    for service in services:
        visa_service = AgencyService(
            agency=visa_agency,
            service=service,
        )
        visa_service.save()
    cities = choices(City.objects.all(), k=randint(1, 3))
    for city in cities:
        agency_office = Office(
            city=city,
            agency=visa_agency,
            address=f.address(),
            contact=f.phone_number()
        )
        agency_office.save()
