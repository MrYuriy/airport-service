from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket,
)

User = get_user_model()


class AirportViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("airport:airport-list")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com",
        )
        self.client = APIClient()  # Create a new client
        self.client.force_authenticate(user=self.admin_user)  # Authenticate the client

    def test_create_airport(self):
        data = {
            "name": "Test Airport",
            "closest_big_city": "Test City",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 1)
        airport = Airport.objects.get()
        self.assertEqual(airport.name, "Test Airport")
        self.assertEqual(airport.closest_big_city, "Test City")

    def test_list_airports(self):
        Airport.objects.create(name="Airport 1", closest_big_city="City 1")
        Airport.objects.create(name="Airport 2", closest_big_city="City 2")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class RouteViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("airport:route-list")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.airport1 = Airport.objects.create(
            name="Airport 1", closest_big_city="City 1"
        )
        self.airport2 = Airport.objects.create(
            name="Airport 2", closest_big_city="City 2"
        )

    def test_create_route(self):
        data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 100,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 1)
        route = Route.objects.get()
        self.assertEqual(route.source, self.airport1)
        self.assertEqual(route.destination, self.airport2)
        self.assertEqual(route.distance, 100)

    def test_list_routes(self):
        Route.objects.create(
            source=self.airport1, destination=self.airport2, distance=100
        )
        Route.objects.create(
            source=self.airport2, destination=self.airport1, distance=200
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class CrewViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("airport:crew-list")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.crew_member = Crew.objects.create(first_name="John", last_name="Doe")

    def test_create_crew_member(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Crew.objects.count(), 2
        )  # Check that a new crew member was created
        self.assertEqual(response.data["first_name"], "Jane")
        self.assertEqual(response.data["last_name"], "Smith")

    def test_create_duplicate_crew_member(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "A crew member with the same first name and last name already exists.",
            str(response.data),  # Convert response data to a string for comparison
        )

    def test_list_crew_members(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # There should be one crew member in the list

    def test_retrieve_crew_member(self):
        url = reverse("airport:crew-detail", args=[self.crew_member.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")


class FlightViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("airport:flight-list")
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane 1",
            rows=10,
            seats_in_row=6,
            air_plane_type=self.airplane_type,
        )
        self.route = Route.objects.create(
            source=Airport.objects.create(name="Source Airport"),
            destination=Airport.objects.create(name="Destination Airport"),
            distance=100,
        )

    def test_create_flight(self):
        data = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": "2023-09-15T10:00:00Z",
            "arrival_time": "2023-09-15T12:00:00Z",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Flight.objects.count(), 1
        )  # Check that a new flight was created
        self.assertEqual(response.data["route"], self.route.id)
        self.assertEqual(response.data["airplane"], self.airplane.id)

    def test_list_flights(self):
        Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2023-09-15T10:00:00Z",
            arrival_time="2023-09-15T12:00:00Z",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # There should be one flight in the list

    def test_retrieve_flight(self):
        # Create a flight instance
        flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2023-09-10T10:00:00Z",
            arrival_time="2023-09-10T12:00:00Z",
        )

        # Get the flight detail via API
        response = self.client.get(reverse("airport:flight-detail", args=[flight.id]))

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Compare the route data as an OrderedDict
        expected_route_data = {
            "id": self.route.id,
            "source": self.route.source.id,
            "destination": self.route.destination.id,
            "distance": self.route.distance,
        }

        self.assertEqual(response.data["route"], expected_route_data)

        self.assertEqual(response.data["airplane"]["id"], self.airplane.id)

        self.assertEqual(response.data["departure_time"], "2023-09-10T10:00:00Z")
        self.assertEqual(response.data["arrival_time"], "2023-09-10T12:00:00Z")


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create airports
        self.source_airport = Airport.objects.create(
            name="Source Airport", closest_big_city="City 1"
        )
        self.destination_airport = Airport.objects.create(
            name="Destination Airport", closest_big_city="City 2"
        )

        # Create a route
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=100,
        )

        # Create an airplane type
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")

        # Create an airplane
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            air_plane_type=self.airplane_type,  # Provide the air_plane_type
        )

        # Create a flight instance
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2023-09-10T10:00:00Z",
            arrival_time="2023-09-10T12:00:00Z",
        )

    def test_create_order(self):
        # Create a ticket instance with valid row and seat values
        ticket_data = {
            "row": 1,  # Change to a valid row value
            "seat": 1,  # Change to a valid seat value
            "flight": self.flight.id,
        }

        # Create an order with the ticket
        order_data = {
            "tickets": [ticket_data],
        }

        response = self.client.post(
            reverse("airport:order-list"), order_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        order = Order.objects.get()
        ticket = Ticket.objects.get()

        self.assertEqual(order.user, self.user)
        self.assertEqual(ticket.flight, self.flight)
        self.assertEqual(ticket.row, ticket_data["row"])
        self.assertEqual(ticket.seat, ticket_data["seat"])

    def test_list_orders(self):
        # Create orders for the user
        order1 = Order.objects.create(user=self.user)
        order2 = Order.objects.create(user=self.user)

        # Create an order for another user
        User.objects.create_user(
            username="otheruser",
            password="otherpassword",
            email="other@example.com",
        )
        Order.objects.create(user=User.objects.get(username="otheruser"))

        response = self.client.get(reverse("airport:order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        response_order_ids = [order["id"] for order in response.data["results"]]
        self.assertIn(order1.id, response_order_ids)
        self.assertIn(order2.id, response_order_ids)
