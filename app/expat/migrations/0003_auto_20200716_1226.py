# Generated by Django 3.0.7 on 2020-07-16 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expat', '0002_auto_20200716_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visaquoterequestmodel',
            name='expat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='expat.ExpatModel'),
        ),
    ]
