import pytest
from faker import Faker
from src.application.auth_module.models import User
from dotenv import load_dotenv
load_dotenv('.env')

fake = Faker()
# Faker.seed(0)

@pytest.mark.django_db
def test_create_user():

    user = User.objects.create(
        email=fake.email(),
        password="123456"
    )
    user.roles.add(1)
    assert user.createdAt != None
