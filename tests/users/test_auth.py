import datetime

import httpx
from django.test import TestCase, Client

from apps.users.models import User, DoctorProfile, PatientProfile


class TestAuthentication(TestCase):
    @classmethod
    def setUp(cls):
        doctor_user = User.objects.create_user(
            username='doctor', email='doctor@email.com', password='doctor_password', role='doctor'
        )

        cls.doctor = DoctorProfile.objects.create(user=doctor_user)

        res = httpx.get("https://api-adresse.data.gouv.fr/search/?q=16+rue+du+paraclet+77160")
        address = res.json()["features"][0]["properties"]["label"]
        patient_user = User.objects.create_user(
            username='patient', email='patient@email.com', password='patient_password'
        )
        cls.patient = PatientProfile.objects.create(
            user=patient_user,
            address=address,
            birth_date=datetime.date(year=1995, month=2, day=18)
        )

        cls.doctor.patients.add(cls.patient)
        cls.doctor.save()

    def test_doctor_authentication(self):
        res = self.client.get("http://127.0.0.1:8000/")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.doctor)

        result = self.client.login(username=self.doctor.get_username(), password='doctor_password')
        self.assertTrue(result)

        self.client.logout()

    def test_user_authentication(self):
        result = self.client.login(
            username=self.patient.get_username(), password='patient_password'
        )
        self.assertTrue(result)
        self.client.logout()