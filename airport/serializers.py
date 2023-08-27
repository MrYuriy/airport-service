from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    Crew,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(
        read_only=True
    )
    destination = AirportSerializer(
        read_only=True
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")

    def validate(self, data):
        """
        Check if a crew with the same first_name and last_name already exists.
        """
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        existing_crew = Crew.objects.filter(first_name=first_name, last_name=last_name).first()
        if existing_crew:
            raise serializers.ValidationError("A crew member with the same first name and last name already exists.")

        return data
