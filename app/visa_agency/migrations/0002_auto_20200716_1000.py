# Generated by Django 3.0.7 on 2020-07-16 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
        ('visa_agency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visaagencymodel',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.Subscription'),
        ),
    ]
