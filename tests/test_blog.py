import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import *
from authentication.models import CustomUser

@pytest.fixture
def api_client():
    client=APIClient()
    client.force_authenticate()
    return client
@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        full_name="Yaw Sarfo",
        username="yaw@gmil.com",
        password="sarfo2021"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Backend Engineering",
        slug="backend",
    )

@pytest.fixture
def tag(db):
    return Tag.objects.create(
        name="django",
        slug="dj",
    )



@pytest.mark.django_db
def test_get_posts(api_client, user):  
    url = reverse("post")
    api_client.force_authenticate(user=user)  

    response = api_client.get(url)

    print("Status Code:", response.status_code)
    print("Response Data:", response.data)

    assert response.status_code == 200
    assert response.data["success"] is True




@pytest.mark.django_db
def test_create_post(api_client, user, category, tag):
    url = reverse("post")
    payload = {
        "title": "first post",
        "content": "This is the body of the post.",  
        "category_id": category.id,
        "tag_ids": [tag.id],
        "is_featured": True
    }
    api_client.force_authenticate(user=user)

    response = api_client.post(url, data=payload)

    print("Status Code:", response.status_code)
    print("Response Data:", response.data)

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["message"] == "Post created successfully"

@pytest.mark.django_db
def test_unauthenticated_posts(category, tag):
    url = reverse("post")
    payload = {
        "title": "Unauthorized post attempt",
        "content": "No user is authenticated.",
        "category_id": category.id,
        "tag_ids": [tag.id],
        "is_featured": False
    }
    client=APIClient()
    response = client.post(url)

    print("Status Code (Unauthenticated):", response.status_code)
    print("Response Data:", response.data)

    assert response.status_code == 401 


@pytest.mark.django_db
def test_create_post_missing_fields(api_client, user, category):
    url = reverse("post")
    payload = {
        "content": "Content without title",
        "category_id": category.id,
        "tag_ids": [],
        "is_featured": False
    }
    api_client.force_authenticate(user=user)

    response = api_client.post(url, data=payload)

    print("Validation Errors:", response.data.get("errors"))

    assert response.status_code == 400
    assert "title" in response.data.get("errors", {})

