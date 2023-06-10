import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from announcement.api.serializers.announcement_serializer import AnnouncementSerializer
from announcement.models import Announcement
from users.models import User


@pytest.mark.django_db
class TestAnnouncementViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testsuperuser", password="testpassword"
        )

    @pytest.fixture
    def super_user(self):
        return User.objects.create_superuser(
            username="testuser", password="testpassword"
        )

    @pytest.fixture
    def announcement(self, user):
        announcement = Announcement.objects.create(
            title="Test Announcement", content="Test content", created_by=user
        )
        return announcement

    def test_retrieve_announcement(self, api_client, announcement):
        response = api_client.get(
            reverse("announcement:announcement-detail", kwargs={"pk": announcement.id})
        )
        assert response.status_code == status.HTTP_200_OK
        assert announcement.view_count + 1 == response.data["view_count"]

    def test_update_announcement(self, api_client, announcement, user):
        new_title = "Updated Announcement"
        new_content = "Updated content"
        data = {"title": new_title, "content": new_content}
        api_client.force_authenticate(user)
        response = api_client.put(
            reverse("announcement:announcement-detail", kwargs={"pk": announcement.id}),
            data,
        )
        assert response.status_code == status.HTTP_200_OK
        announcement.refresh_from_db()
        assert announcement.title == new_title
        assert announcement.content == new_content

    def test_delete_announcement(self, api_client, user):
        announcement = Announcement.objects.create(
            title="Test Announcement", content="Test content", created_by=user
        )
        api_client.force_authenticate(user)
        response = api_client.delete(
            reverse("announcement:announcement-detail", kwargs={"pk": announcement.id})
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Announcement.objects.filter(id=announcement.id).exists()

    def test_accept_announcement(self, api_client, announcement, user, super_user):
        assert announcement.approved is False

        api_client.force_authenticate(user)
        response = api_client.post(
            reverse("announcement:announcement-accept", kwargs={"pk": announcement.id})
        )

        announcement.refresh_from_db()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert announcement.approved is False

        api_client.force_authenticate(super_user)
        response = api_client.post(
            reverse("announcement:announcement-accept", kwargs={"pk": announcement.id})
        )
        announcement.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert announcement.approved is True
