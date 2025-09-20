from django.contrib import admin
from django.db.models import Count
from .models import (
    Play, Actor, Genre,
    TheatreHall, Performance,
    Reservation, Ticket
)


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "get_genres", "get_actors")
    search_fields = ("title", "description")
    list_filter = ("genres", "actors")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("genres", "actors")

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = "Genres"

    def get_actors(self, obj):
        return ", ".join([actor.full_name for actor in obj.actors.all()])
    get_actors.short_description = "Actors"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")
    list_filter = ("last_name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row")
    readonly_fields = ("rows", "seats_in_row")
    search_fields = ("name",)
    list_filter = ("rows",)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("play", "theatre_hall", "show_time", "tickets_count")
    readonly_fields = ("tickets_count",)
    search_fields = ("play__title", "theatre_hall__name")
    list_filter = ("show_time", "theatre_hall")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("play", "theatre_hall").annotate(
            _tickets_count=Count("tickets")
        )

    def tickets_count(self, obj):
        return obj._tickets_count
    tickets_count.short_description = "Tickets Sold"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)
    list_filter = ("created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user").prefetch_related(
            "tickets__performance__play",
            "tickets__performance__theatre_hall"
        )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("performance", "row", "seat", "reservation")
    search_fields = ("row", "seat",)
    list_filter = ("performance", "reservation",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("performance", "reservation")
