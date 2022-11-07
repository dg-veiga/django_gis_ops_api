from django.urls import path
from .views.user_area import UserAreaCreateView
from .views.general import health

urlpatterns = [
    path("user_area/", UserAreaCreateView.as_view(), name="user-area-list-create"),
    path("health/", health, name="index"),
]
