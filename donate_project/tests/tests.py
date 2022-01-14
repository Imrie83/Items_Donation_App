import pytest
from django.contrib import auth
from django.contrib.auth.models import User

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
    assert len(Institution.objects.all()) == 3


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
    assert response.context['supported'] == 3
    assert response.context['bag_count'] == 12


@pytest.mark.django_db
def test_dynamic_institutions(client, create_institute):
    response = client.get('/')
    fun = Institution.objects.get(type=1)
    org = Institution.objects.get(type=2)
    loc = Institution.objects.get(type=3)

    assert len(response.context['foundation']) == 1
    assert len(response.context['organization']) == 1
    assert len(response.context['local_collection']) == 1
    assert fun.name == 'Inst 1'
    assert org.name == 'Inst 2'
    assert loc.name == 'Inst 3'


@pytest.mark.django_db
def test_register_user(client):
    assert len(User.objects.all()) == 0

    response = client.post(
        '/register/',
        {
            'name': 'Marcin',
            'surname': 'Nazwisko',
            'email': 'test@google.com',
            'password': 'test',
            'password2': 'test',
        }
    )

    assert response.status_code == 302
    assert len(User.objects.all()) == 1

    user = User.objects.last()
    assert user.email == 'test@google.com'


@pytest.mark.django_db
def test_login_user(client, create_user):
    assert User.objects.get(email='test@gmail.com')

    response = client.post(
        '/login/',
        {
            'username': 'test@gmail.com',
            'password': 'test',
        }
    )
    assert response.status_code == 302
    assert '/' in response.url


@pytest.mark.django_db
def test_logout_user(client, create_user):
    user = client.force_login(create_user[0])
    assert auth.get_user(client).username == 'test@gmail.com'
    client.logout()
    assert auth.get_user(client).username == ''
