from io import StringIO

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from users.models import CustomUser
from users.fake import create_user
from core.models import City, Service
from visa_agency.fake import create_visa_agency, create_visa_agency_prospect
from subscription.models import create_free_leads_subscription_type, create_time_subscription_type


class Command(BaseCommand):
    help = "Populate database with test objects"
    placeholders_dir = "saleor/static/placeholders/"

    def add_arguments(self, parser):

        parser.add_argument(
            "--createsuperuser",
            action="store_true",
            dest="createsuperuser",
            default=False,
            help="Create admin account",
        )

        parser.add_argument(
            "--subscriptions",
            action="store_true",
            dest="subscriptions",
            default=False,
            help="Create admin account",
        )

    def make_database_faster(self):
        """Sacrifice some of the safeguards of sqlite3 for speed.

        Users are not likely to run this command in a production environment.
        They are even less likely to run it in production while using sqlite3.
        """
        if "sqlite3" in connection.settings_dict["ENGINE"]:
            cursor = connection.cursor()
            cursor.execute("PRAGMA temp_store = MEMORY;")
            cursor.execute("PRAGMA synchronous = OFF;")

    def create_superuser(self, credentials):
        user, created = CustomUser.objects.get_or_create(
            email=credentials["email"],
            defaults={"is_active": True, "is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password(credentials["password"])
            user.save()
            msg = "Superuser - %(email)s/%(password)s" % credentials
        else:
            msg = "Superuser already exists - %(email)s" % credentials
        return msg

    def handle(self, *args, **options):
        self.make_database_faster()
        if options["createsuperuser"]:
            credentials = {"email": "vlad@admin.com", "password": "123"}
            msg = self.create_superuser(credentials)
            self.stdout.write(msg)

        if options["subscriptions"]:
            create_free_leads_subscription_type(10)
            create_time_subscription_type(30, 44)
            create_time_subscription_type(90, 99)
            self.stdout.write('Created subscriptions')

        city_list = ['Danang', 'Ho Chi Minh', 'Hanoi', 'Nha Trang', 'Hoi An', 'Dalat']
        service_list = ['Visa Extension 1 month', 'Visa Extension 2 month', 'Visa Extension 3 month', 'Business Visa',
                        'Visa Letter']
        for city in city_list:
            City.objects.create(name=city)
        for service in service_list:
            Service.objects.create(name=service)
        self.stdout.write('Created cities and services')

        for i in range(20):
            create_visa_agency()
        self.stdout.write('Created 20 visa agencies')
        for i in range(30):
            create_visa_agency_prospect()
        self.stdout.write('Created 30 visa agencies prospects')
