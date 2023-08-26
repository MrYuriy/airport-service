from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.models import Airport
from airport.serializers import (
    AirportSerializer,
)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
