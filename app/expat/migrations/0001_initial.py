# Generated by Django 3.0.7 on 2020-07-16 09:58

from django.db import migrations, models
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('subscribed', models.BooleanField(default=True)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=128, null=True)),
                ('name', models.CharField(max_length=128)),
                ('nationality', django_countries.fields.CountryField(max_length=746, multiple=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('issue_place', models.CharField(max_length=128)),
                ('issue_date', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
                ('entry_date', models.DateTimeField()),
                ('entry_port', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='VisaQuoteRequestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('persons', models.IntegerField(default=1)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VisaQuoteResponseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(help_text='Price in USD')),
                ('duration', models.IntegerField(help_text='How many days it will take')),
                ('note', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
