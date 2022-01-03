import pytest
from donate_app.models import Category, Institution, Donation


@pytest.fixture
def create_categories():
    cat_1 = Category.objects.update_or_create(
        name='Category 1'
    )
    cat_2 = Category.objects.update_or_create(
        name='Category 2'
    )
    cat_3 = Category.objects.update_or_create(
        name='Category 3'
    )
    return [cat_1, cat_2, cat_3]


@pytest.fixture
def create_institute():
    institute_1 = Institution.objects.update_or_create(
        name='Inst 1',
        type=1,
    )
    institute_2 = Institution.objects.update_or_create(
        name='Inst 2',
        type=2,
    )
