from rest_framework import serializers

from announcement.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Announcement
        fields = (
            "id",
            "title",
            "content",
            "created_by",
            "created_at",
            "updated_at",
            "publish_at",
            "approved",
            "view_count",
        )
        read_only_fields = ("created_at", "updated_at", "approved", "view_count")
