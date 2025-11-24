from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import SpyCat, Mission, Target, Note


class SpyCatAgencyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.spy_cat = SpyCat.objects.create(
            name="Tom",
            year_of_experience=3,
            breed="Siamese",
            salary=1500.0
        )

    def test_create_spy_cat(self):
        data = {
            "name": "Jerry",
            "year_of_experience": 2,
            "breed": "Persian",
            "salary": 1200.0
        }
        response = self.client.post("/api/spycats/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpyCat.objects.count(), 2)

    def test_update_spy_cat_salary(self):
        data = {"salary": 2000.0}
        response = self.client.patch(f"/api/spycats/{self.spy_cat.id}/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.spy_cat.refresh_from_db()
        self.assertEqual(float(self.spy_cat.salary), 2000.0)

    def test_delete_spy_cat(self):
        response = self.client.delete(f"/api/spycats/{self.spy_cat.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SpyCat.objects.count(), 0)


    def test_create_mission_with_targets(self):
        data = {
            "cat": self.spy_cat.id,
            "complete_state": False,
            "targets": [
                {"name": "Target 1", "country": "Ukraine", "complete_state": False},
                {"name": "Target 2", "country": "Poland", "complete_state": False}
            ]
        }
        response = self.client.post("/api/missions/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mission.objects.count(), 1)
        self.assertEqual(Target.objects.count(), 2)

    def test_mission_complete_when_all_targets_complete(self):
        mission = Mission.objects.create(cat=self.spy_cat, complete_state=False)
        t1 = Target.objects.create(name="T1", country="UA", complete_state=False, mission=mission)
        t2 = Target.objects.create(name="T2", country="PL", complete_state=False, mission=mission)

        t1.complete_state = True
        t1.save()
        mission.refresh_from_db()
        self.assertFalse(mission.complete_state)

        t2.complete_state = True
        t2.save()
        mission.refresh_from_db()
        self.assertTrue(mission.complete_state)
