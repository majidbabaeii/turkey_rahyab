from django.conf import settings
from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]
