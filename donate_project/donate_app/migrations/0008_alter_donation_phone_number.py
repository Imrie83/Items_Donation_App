# Generated by Django 4.0 on 2022-01-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate_app', '0007_donation_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=255, null=True, verbose_name='Telefon'),
        ),
    ]
