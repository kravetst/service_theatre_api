from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from datetime import datetime, timezone

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Ticket, Reservation
from theatre.serializers import (
    TicketSerializer,
    ReservationSerializer,
    ReservationListSerializer,
    PerformanceDetailSerializer,
    PerformanceListSerializer,
    PlayDetailSerializer,
)


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.hall = TheatreHall.objects.create(name="Small Hall", rows=2, seats_in_row=2)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 12, 1, 19, 0, tzinfo=timezone.utc),
        )

    def test_valid_ticket(self):
        data = {"row": 1, "seat": 1, "performance": self.performance.id}
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_ticket_out_of_range(self):
        data = {"row": 3, "seat": 1, "performance": self.performance.id}
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class PerformanceSerializerTest(TestCase):
    def setUp(self):
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.hall = TheatreHall.objects.create(name="Main Hall", rows=2, seats_in_row=2)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 12, 1, 19, 0, tzinfo=timezone.utc),
        )

    def test_performance_list_tickets_available(self):
        Ticket.objects.create(row=1, seat=1, performance=self.performance)
        serializer = PerformanceListSerializer(self.performance)
        self.assertEqual(serializer.data["tickets_available"], 3)

    def test_performance_detail_taken_places(self):
        Ticket.objects.create(row=1, seat=1, performance=self.performance)
        serializer = PerformanceDetailSerializer(self.performance)
        self.assertEqual(len(serializer.data["taken_places"]), 1)


class ReservationSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.hall = TheatreHall.objects.create(name="Small Hall", rows=2, seats_in_row=2)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 12, 1, 19, 0, tzinfo=timezone.utc),
        )

    def test_reservation_create_with_multiple_tickets(self):
        data = {
            "tickets": [
                {"row": 1, "seat": 1, "performance": self.performance.id},
                {"row": 1, "seat": 2, "performance": self.performance.id},
            ]
        }
        serializer = ReservationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        reservation = serializer.save(user=self.user)
        self.assertEqual(reservation.tickets.count(), 2)

    def test_reservation_fails_on_taken_seat(self):
        Ticket.objects.create(row=1, seat=1, performance=self.performance)
        data = {"tickets": [{"row": 1, "seat": 1, "performance": self.performance.id}]}
        serializer = ReservationSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_reservation_list_serializer(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(row=1, seat=1, performance=self.performance, reservation=reservation)
        serializer = ReservationListSerializer(reservation)
        self.assertEqual(len(serializer.data["tickets"]), 1)