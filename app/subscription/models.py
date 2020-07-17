from django.db import models


class SUBTYPE(models.TextChoices):
    LEADS = 'LL', 'Leads Limited'
    DAYS = 'DL', 'Date Limited'


class SUBSTATUS(models.TextChoices):
    ACTIVE = ('A', 'Active')
    EXPIRED = ('E', 'Expired')
    PENDING = ('P', 'Pending')


class SubscriptionType(models.Model):
    name = models.CharField(max_length=128)
    idx = models.CharField(db_index=True, max_length=8, unique=True)
    type = models.CharField(
        max_length=2,
        choices=SUBTYPE.choices,
        default=SUBTYPE.LEADS
    )
    price = models.FloatField(blank=True, null=True)
    description = models.TextField()
    leads = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f'{self.name}-{self.type}'


class Subscription(models.Model):
    type = models.ForeignKey(SubscriptionType, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    leads = models.IntegerField()
    status = models.CharField(
        max_length=2,
        choices=SUBSTATUS.choices,
        default=SUBSTATUS.PENDING
    )

    def __str__(self):
        return f'{self.type.name}-{self.type.type}'


def create_free_leads_subscription_type(leads:int):
    sub = SubscriptionType(
        idx='freeleads',
        name='Free',
        description=f'see and respond to {leads} quote requests',
        leads=leads,
    )
    sub.save()
    return sub


def create_free_time_subscription_type(days: int):
    sub = SubscriptionType(
        idx=f'freetime',
        name=f'{days} days',
        description=f'unlimited responses to quotes for {days} days',
        duration=days,
        type=SUBTYPE.DAYS
    )
    sub.save()
    return sub


def create_time_subscription_type(days: int, price: int):
    sub = SubscriptionType(
        idx=f'{days}days',
        name=f'{days} days',
        description=f'unlimited responses to quotes for {days} days',
        price=price,
        duration=days,
        type=SUBTYPE.DAYS
    )
    sub.save()
    return sub
