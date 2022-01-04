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


@pytest.mark.django_db
def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_view(client):
    response = client.get('/login/')
    assert response.status_code == 200


def test_register_view(client):
    response = client.get('/register/')
    assert response.status_code == 200


def test_donate_view(client):
    response = client.get('/donate/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_dynamic_stat(client, create_donations):
    response = client.get('/')
    assert response.context['supported'] == 2
    assert response.context['bag_count'] == 12
