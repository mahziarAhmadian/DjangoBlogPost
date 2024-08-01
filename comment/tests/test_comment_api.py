from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User, Profile
from blog.models.posts import Post
from comment.models.comments import Comment


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(phone_number="09121111111", password="1234")
    return user


@pytest.fixture
def super_admin():
    User.objects.create_superuser(phone_number="09125555555", password="1234")
    user_obj = User.objects.get(phone_number="09125555555")
    user_obj.permissions = ["ListPosts", "CreatePost"]
    user_obj.save()
    return user_obj


@pytest.fixture
def test_post(common_user):
    author = Profile.objects.get(user=common_user)
    post = Post.objects.create(
        author=author,
        title="TestPost",
        content="",
        status=True,
        published_date=datetime.now(),
    )
    return post.id


@pytest.mark.django_db
class TestPostApi:

    def test_create_comment_response_201_status(
        self, api_client, common_user, test_post
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("comments:api-v1-comment:create-comment")
        user_profile = Profile.objects.get(user=common_user).id
        data = {
            "post": test_post,
            "user_profile": user_profile,
            "content": "this is test comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_comment_response_401_status(
        self, api_client, common_user, test_post
    ):
        url = reverse("comments:api-v1-comment:create-comment")
        user_profile = Profile.objects.get(user=common_user).id
        data = {
            "post": test_post,
            "user_profile": user_profile,
            "content": "this is test comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_update_comment_response_200_status(
        self, api_client, common_user, test_post
    ):
        # first create fake comment .
        api_client.force_authenticate(user=common_user)
        url = reverse("comments:api-v1-comment:create-comment")
        user_profile = Profile.objects.get(user=common_user).id
        data = {
            "post": test_post,
            "user_profile": user_profile,
            "content": "this is test comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

        # edite fake comment message .
        comment_id = Comment.objects.get(
            post=response.data["post"],
            user_profile=user_profile,
            content=response.data["content"],
        ).id
        update_data = {"content": "comment edited "}
        update_url = reverse(
            "comments:api-v1-comment:comment-update-destroy", kwargs={"pk": comment_id}
        )
        update_response = api_client.put(update_url, update_data)
        assert update_response.status_code == 200

    def test_delete_comment_response_204_status(
        self, api_client, common_user, test_post
    ):
        # first create fake comment .
        api_client.force_authenticate(user=common_user)
        url = reverse("comments:api-v1-comment:create-comment")
        user_profile = Profile.objects.get(user=common_user).id
        data = {
            "post": test_post,
            "user_profile": user_profile,
            "content": "this is test comment",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

        # delete fake comment message .
        comment_id = Comment.objects.get(
            post=response.data["post"],
            user_profile=user_profile,
            content=response.data["content"],
        ).id

        delete_url = reverse(
            "comments:api-v1-comment:comment-update-destroy", kwargs={"pk": comment_id}
        )
        delete_response = api_client.delete(delete_url)
        assert delete_response.status_code == 204
