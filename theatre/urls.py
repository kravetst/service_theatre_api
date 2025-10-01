from django.urls import include, path
from rest_framework.routers import DefaultRouter
from theatre.views import (
    PlayViewSet,
    ActorViewSet,
    GenreViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet
)

app_name = "theatre"
router = DefaultRouter()
router.register("plays", PlayViewSet, basename="play")
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]