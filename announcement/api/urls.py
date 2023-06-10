from django.urls import include, path
from rest_framework import routers

from announcement.api.views import AnnouncementViewSet, MyAnnouncementViewSet

router = routers.DefaultRouter()
router.register(r"announcements", AnnouncementViewSet, basename="announcement")
router.register(r"my-announcements", MyAnnouncementViewSet, basename="my-announcement")

app_name = "announcement"
urlpatterns = [
    path("", include(router.urls)),
]
