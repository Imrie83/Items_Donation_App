# Generated by Django 4.0 on 2022-01-03 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donate_app', '0005_rename_donation_donation_institution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='institution',
        ),
    ]
