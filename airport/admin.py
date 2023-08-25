from django.contrib import admin
from .models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Ticket,
    Order,
)


class AirportModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'closest_big_city')
    list_filter = ('closest_big_city',)
    search_fields = ('name', 'closest_big_city')


class RouteModelAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'distance')


class CrewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_in_row', 'air_plane_type')


class FlightAdmin(admin.ModelAdmin):
    list_display = ('route', 'airplane', 'departure_time', 'arrival_time', 'duration')
    list_filter = ('route', 'airplane')
    date_hierarchy = 'departure_time'


class TicketAdmin(admin.ModelAdmin):
    list_display = ('flight', 'row', 'seat')
    list_filter = ('flight',)
    search_fields = ('flight__route__source__name', 'flight__route__destination__name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user')
    list_filter = ('user',)
    date_hierarchy = 'created_at'


admin.site.register(Airport, AirportModelAdmin)
admin.site.register(Route, RouteModelAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(AirplaneType, AirplaneTypeAdmin)
admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Order, OrderAdmin)
