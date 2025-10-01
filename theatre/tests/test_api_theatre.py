from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import tempfile
import os
from PIL import Image
from datetime import datetime, timezone

from theatre.models import Play, TheatreHall, Performance, Ticket, Reservation


class PlayAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")

    def test_get_play_list(self):
        response = self.client.get("/api/theatre/plays/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Hamlet", [item["title"] for item in response.json()])

    def test_create_play(self):
        data = {"title": "Othello", "description": "Tragedy by Shakespeare"}
        response = self.client.post("/api/theatre/plays/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Play.objects.filter(title="Othello").exists())


class ReservationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="pass1234"
        )
        self.client.force_authenticate(user=self.user)
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.hall = TheatreHall.objects.create(name="Small Hall", rows=2, seats_in_row=2)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 12, 1, 19, 0, tzinfo=timezone.utc),
        )
        self.reservation = Reservation.objects.create(user=self.user)

    def test_create_reservation_api(self):
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "performance": self.performance.id,
                    "reservation": self.reservation.id,
                }
            ]
        }
        response = self.client.post("/api/theatre/reservations/", payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])


class PerformanceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="pass1234"
        )
        self.client.force_authenticate(user=self.user)
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.hall = TheatreHall.objects.create(name="Main Hall", rows=2, seats_in_row=2)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=datetime(2025, 12, 1, 19, 0, tzinfo=timezone.utc),
        )
        self.reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(
            row=1, seat=1, performance=self.performance, reservation=self.reservation
        )

    def test_performance_list_tickets_available(self):
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        performance_data = response.json()[0]
        self.assertEqual(performance_data["theatre_hall_capacity"], 4)
        self.assertEqual(performance_data["tickets_available"], 3)


class PlayImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.play = Play.objects.create(title="Hamlet", description="Tragedy")
        self.url = reverse("theatre:play-upload-image", args=[self.play.id])

    def tearDown(self):
        if self.play.image:
            if os.path.exists(self.play.image.path):
                os.remove(self.play.image.path)

    def test_upload_image_to_play(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            img = Image.new("RGB", (10, 10))
            img.save(temp_image, format="JPEG")
            temp_image.seek(0)

            res = self.client.post(self.url, {"image": temp_image}, format="multipart")

        self.play.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.play.image.path))
