from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.models import Airport, Route, Crew
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    CrewSerializer,
)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.all().prefetch_related("source", "destination")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(source__name__icontains=source)

        if destination:
            queryset = queryset.filter(genres__name__icontains=destination)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
