import pytest
from donate_app.models import (
    Category,
    Institution,
    Donation,
)

@pytest.mark.django_db
def test_category(client, create_categories):
    assert Category.objects.get(name='Category 1')
    assert len(Category.objects.all()) == 3


@pytest.mark.django_db
def test_institute(client, create_institute):
    assert Institution.objects.get(name='Inst 1')
    assert len(Institution.objects.all()) == 2
