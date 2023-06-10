import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from announcement.api.serializers.announcement_serializer import AnnouncementSerializer
from announcement.models import Announcement
from users.models import User


@pytest.mark.django_db
class TestMyAnnouncementViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpassword")

    @pytest.fixture
    def my_announcement(self, user):
        announcement = Announcement.objects.create(
            title="My Announcement", content="My content", created_by=user
        )
        return announcement

    def test_retrieve_my_announcement(self, api_client, user, my_announcement):
        api_client.force_authenticate(user=user)
        response = api_client.get(
            reverse(
                "announcement:my-announcement-detail", kwargs={"pk": my_announcement.id}
            )
        )

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_my_announcement_unauthenticated(
        self, api_client, my_announcement
    ):
        response = api_client.get(
            reverse(
                "announcement:my-announcement-detail", kwargs={"pk": my_announcement.id}
            )
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_my_announcement_other_user(
        self, api_client, user, my_announcement
    ):
        other_user = User.objects.create_user(
            username="otheruser", password="testpassword"
        )
        api_client.force_authenticate(user=other_user)
        response = api_client.get(
            reverse(
                "announcement:my-announcement-detail", kwargs={"pk": my_announcement.id}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
