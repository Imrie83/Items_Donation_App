from django.contrib.auth.models import User
from django.db import models

ORGANIZATIONS = [
    (1, 'Fundacja'),
    (2, 'Organizacja pozarządowa'),
    (3, 'Zbiórka lokalna'),
]


class Category(models.Model):
    """
    Class creates a model storing Categories names.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Nazwa',
        null=False,
        unique=True,
    )


class Institution(models.Model):
    """
    Class creates a model storing information regarding available institutions.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Nazwa Instytucji',
        null=False,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Opis',
        null=True,
    )
    type = models.CharField(
        max_length=255,
        choices=ORGANIZATIONS,
        default=ORGANIZATIONS[0],
        null=False,
        verbose_name='Typ',
    )
    category = models.ManyToManyField(
        to=Category,
        verbose_name='Kategoria',
        related_name='institution',
    )


class Donation(models.Model):
    """
    Class creates a model storing information regarding a donation.
    """
    quantity = models.IntegerField(
        verbose_name='Ilość',
        null=False,
    )
    category = models.ManyToManyField(
        to=Category,
        verbose_name='Kategoria',
    )
    institution = models.ForeignKey(
        to=Institution,
        verbose_name='Instytucja',
        name='institution',
        null=True,
        on_delete=models.SET(None),
        related_name='donation'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Adres',
        null=True,
    )
    phone_number = models.IntegerField(
        verbose_name='Telefon',
        null=True,
    )
    city = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Miasto',
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='Kod pocztowy',
        null=True,
    )
    pick_up_date = models.DateField(
        verbose_name='Data odbioru',
        null=False,
    )
    pick_up_time = models.TimeField(
        verbose_name='Godzina odbioru',
        null=False
    )
    pick_up_comment = models.TextField(
        verbose_name='Komentarz',
        null=True,
    )
    user = models.ForeignKey(
        to=User,
        null=True,
        default=None,
        verbose_name='Użytkownik',
        on_delete=models.SET(None),
    )
