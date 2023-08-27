from django.urls import path, include
from rest_framework import routers


from airport.views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    AirplaneTypeViewSet,
)

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routers", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)

urlpatterns = [
    path("", include(router.urls))
]
app_name = "airport"
