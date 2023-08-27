from django.urls import path, include
from rest_framework import routers


from airport.views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routers", RouteViewSet)
router.register("crews", CrewViewSet)

urlpatterns = [
    path("", include(router.urls))
]
app_name = "airport"
