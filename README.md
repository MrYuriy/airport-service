# Project Description

This project is a Django application for managing aviation data, including airports, routes, crews, airplane types,
airplanes, flights, orders, and tickets.

## Project Structure

The project consists of several files organized as follows:

- **`urls.py`**: This file contains the configuration of Django URL routes using the `router` to provide API endpoints
  for various models.

- **`models.py`**: This file defines the data models used in the project, including `Airport`, `Route`, `Crew`
  , `AirplaneType`, `Airplane`, `Flight`, `Order`, and `Ticket`.

## Description of Models

- **`Airport`**: A model representing an airport with fields `name` (airport name) and `closest_big_city` (closest major
  city).

- **`Route`**: A model representing a route between airports with fields `source` (departure airport), `destination` (
  arrival airport), and `distance` (distance between airports).

- **`Crew`**: A model representing a crew with fields `first_name` (first name) and `last_name` (last name).

- **`AirplaneType`**: A model representing an airplane type with the field `name` (type name).

- **`Airplane`**: A model representing an airplane with fields `name` (name), `rows` (number of rows),
  and `seats_in_row` (number of seats in a row).

- **`Flight`**: A model representing a flight with fields `route` (route), `airplane` (airplane), `departure_time` (
  departure time), and `arrival_time` (arrival time).

- **`Order`**: A model representing an order with fields `created_at` (creation date) and `user` (user).

- **`Ticket`**: A model representing a ticket with fields `flight` (flight), `row` (row), and `seat` (seat).

## Usage

You can use this project to manage data about airports, routes, crews, airplane types, airplanes, flights, orders, and
tickets in an aviation system.

For more information about available API endpoints and methods, refer to the `urls.py` file and the official
documentation of Django REST framework.
