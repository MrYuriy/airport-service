from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
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


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "air_plane_type", "capacity")


class AirplaneListSerializer(AirplaneSerializer):
    air_plane_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "air_plane_type", "capacity")


class AirplaneDetailSerializer(AirplaneSerializer):
    air_plane_type = AirplaneTypeSerializer(
        read_only=True
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "air_plane_type", "capacity")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class FlightListSerializer(FlightSerializer):
    airplane_capacity = serializers.IntegerField(source="airplane.capacity", read_only=True)
    route = serializers.SerializerMethodField("get_route")

    def get_route(self, obj):
        return f"{obj.route.source} - {obj.route.destination}"

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "airplane_capacity"
        )


class FlightDetailSerializer(FlightSerializer):
    route = RouteSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")
