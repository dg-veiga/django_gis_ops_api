from rest_framework import generics

from base.models.user_area import UserArea
from base.api.v1.serializers import UserAreaCreateSerializer


class UserAreaCreateView(generics.ListCreateAPIView):
    queryset = UserArea.objects.filter(is_active=True)
    serializer_class = UserAreaCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserAreaCreateSerializer

    def perform_create(self, serializer):
        user_area = serializer.save()
        area = float(user_area.geometry.area)
        centroid = user_area.geometry.centroid
        serializer.save(area=area, centroid=centroid)
