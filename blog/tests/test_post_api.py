from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def super_admin():
    user_obj = User.objects.create_superuser(
        phone_number="09125555555", password="1234"
    )
    user_obj = User.objects.get(phone_number="09125555555")
    user_obj.permissions = ["ListPosts", "CreatePost"]
    user_obj.save()
    return user_obj


@pytest.mark.django_db
class TestPostApi:
    def test_get_post_response_200_status(self, api_client, super_admin):
        api_client.force_authenticate(user=super_admin)
        url = reverse("blogs:api-v1-blog:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client, super_admin):
        url = reverse("blogs:api-v1-blog:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, super_admin):
        api_client.force_authenticate(user=super_admin)
        url = reverse("blogs:api-v1-blog:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status(
            self, api_client, super_admin
    ):
        url = reverse("blogs:api-v1-blog:post-list")
        data = {"title": "test", "content": "description"}
        user = super_admin

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400
