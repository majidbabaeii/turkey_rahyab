from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from ..models import Announcement
from .permissions import OwnerPermission
from .serializers.announcement_serializer import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = [IsAdminUser | OwnerPermission]

        if self.action in ["accept"]:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.approved = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def views(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({"view_count": instance.view_count})


class MyAnnouncementViewSet(AnnouncementViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
