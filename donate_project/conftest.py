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
    institute_3 = Institution.objects.update_or_create(
        name='Inst 3',
        type=3,
    )


@pytest.fixture
def create_donations(create_institute):
    inst_1 = Institution.objects.first()
    inst_2 = Institution.objects.last()
    donation_1 = Donation.objects.update_or_create(
        quantity=2,
        institution=inst_1,
        pick_up_time='12:12',
        pick_up_date='2022-3-3',
    )
    donation_2 = Donation.objects.update_or_create(
        quantity=3,
        institution=inst_1,
        pick_up_time='12:12',
        pick_up_date='2022-3-3',
    )
    donation_3 = Donation.objects.update_or_create(
        quantity=7,
        institution=inst_2,
        pick_up_time='12:12',
        pick_up_date='2022-3-3',
    )
