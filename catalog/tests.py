from pathlib import Path
from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import ChildProfile, Lullaby, ParentLullabyRecording


User = get_user_model()


class ParentLullabySecurityTests(TestCase):
    def test_user_cannot_use_another_users_child(self):
        user1 = User.objects.create_user(
            username="user1",
            password="testpass123",
        )
        user2 = User.objects.create_user(
            username="user2",
            password="testpass123",
        )

        child2 = ChildProfile.objects.create(
            user=user2,
            name="Child Two",
            birth_date=date(2020, 1, 1),
        )

        lullaby = Lullaby.objects.create(
            title="Test Lullaby",
            slug="test-lullaby",
            description="Test",
        )

        client = APIClient()
        client.force_authenticate(user=user1)

        audio = SimpleUploadedFile(
            "test.webm",
            b"fake audio content",
            content_type="audio/webm",
        )

        response = client.post(
            "/api/lullaby-recordings/",
            {
                "lullaby": lullaby.id,
                "child": child2.id,
                "title": "Unauthorized recording",
                "audio_file": audio,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("child", response.data)

    def test_non_audio_file_is_rejected(self):
        user = User.objects.create_user(
            username="audio_test_user",
            password="testpass123",
        )

        lullaby = Lullaby.objects.create(
            title="Audio Validation Test",
            slug="audio-validation-test",
            description="Test",
        )

        client = APIClient()
        client.force_authenticate(user=user)

        file = SimpleUploadedFile(
            "test.txt",
            b"not an audio file",
            content_type="text/plain",
        )

        response = client.post(
            "/api/lullaby-recordings/",
            {
                "lullaby": lullaby.id,
                "title": "Invalid file",
                "audio_file": file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("audio_file", response.data)

    def test_oversized_audio_file_is_rejected(self):
        user = User.objects.create_user(
            username="large_audio_user",
            password="testpass123",
        )

        lullaby = Lullaby.objects.create(
            title="Large Audio Test",
            slug="large-audio-test",
            description="Test",
        )

        client = APIClient()
        client.force_authenticate(user=user)

        large_audio = SimpleUploadedFile(
            "large.webm",
            b"0" * (10 * 1024 * 1024 + 1),
            content_type="audio/webm",
        )

        response = client.post(
            "/api/lullaby-recordings/",
            {
                "lullaby": lullaby.id,
                "title": "Oversized audio",
                "audio_file": large_audio,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("audio_file", response.data)

    def test_user_cannot_delete_another_users_recording(self):
        user1 = User.objects.create_user(
            username="delete_user1",
            password="testpass123",
        )
        user2 = User.objects.create_user(
            username="delete_user2",
            password="testpass123",
        )

        lullaby = Lullaby.objects.create(
            title="Delete Security Test",
            slug="delete-security-test",
            description="Test",
        )

        recording = ParentLullabyRecording.objects.create(
            user=user2,
            lullaby=lullaby,
            audio_file=SimpleUploadedFile(
                "other-user.webm",
                b"fake audio",
                content_type="audio/webm",
            ),
        )

        client = APIClient()
        client.force_authenticate(user=user1)

        response = client.delete(
            f"/api/lullaby-recordings/{recording.id}/"
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            ParentLullabyRecording.objects.filter(
                id=recording.id
            ).exists()
        )

    def test_user_can_delete_own_recording(self):
        user = User.objects.create_user(
            username="delete_own_user",
            password="testpass123",
        )

        lullaby = Lullaby.objects.create(
            title="Own Delete Test",
            slug="own-delete-test",
            description="Test",
        )

        recording = ParentLullabyRecording.objects.create(
            user=user,
            lullaby=lullaby,
            audio_file=SimpleUploadedFile(
                "own-recording.webm",
                b"fake audio",
                content_type="audio/webm",
            ),
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(
            f"/api/lullaby-recordings/{recording.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            ParentLullabyRecording.objects.filter(
                id=recording.id
            ).exists()
        )


class RecommendationAPITests(TestCase):
    def test_authenticated_user_can_get_own_child_recommendations(self):
        user = User.objects.create_user(
            username="recommendation_user",
            password="testpass123",
        )

        child = ChildProfile.objects.create(
            user=user,
            name="Test Child",
            birth_date=date(2020, 1, 1),
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(
            f"/api/child-profiles/{child.id}/recommendations/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["child"]["id"], child.id)
        self.assertEqual(response.data["child"]["name"], "Test Child")
        self.assertIn("age_months", response.data)
        self.assertIn("recommendations", response.data)

    def test_unauthenticated_user_cannot_get_child_recommendations(self):
        user = User.objects.create_user(
            username="private_recommendation_user",
            password="testpass123",
        )

        child = ChildProfile.objects.create(
            user=user,
            name="Private Child",
            birth_date=date(2020, 1, 1),
        )

        client = APIClient()

        response = client.get(
            f"/api/child-profiles/{child.id}/recommendations/"
        )

        self.assertIn(response.status_code, [401, 403])
