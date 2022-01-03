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
        null=False,
    )
