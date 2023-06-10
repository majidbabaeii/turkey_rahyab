from django.contrib import admin

from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_by",
        "created_at",
        "publish_at",
        "approved",
        "view_count",
    )
    list_filter = ("created_by", "publish_at", "approved")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


admin.site.register(Announcement, AnnouncementAdmin)
