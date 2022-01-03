import pytest
from donate_app.models import (
    Category
)

@pytest.mark.django_db
def test_category(client, create_categories):
    assert Category.objects.get(name='Category 1')
