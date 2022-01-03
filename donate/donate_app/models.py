from django.db import models


class Category(models.Model):
    """
    Class creates a model storing Categories names.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Name',
        null=False,
        default='Name?',
        unique=True,
    )
