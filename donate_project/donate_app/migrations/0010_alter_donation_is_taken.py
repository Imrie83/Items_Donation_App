# Generated by Django 4.0 on 2022-01-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate_app', '0009_alter_institution_options_donation_is_taken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False, verbose_name='Zabrane'),
        ),
    ]
