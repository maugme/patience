import datetime

import httpx
from django.test import TestCase

from apps.users.models import User, DoctorProfile, PatientProfile


class TestAuthentication(TestCase):
    def setUp(self):
        doctor_user = User.objects.create_user(
            username='doctor', email='doctor@email.com', password='doctor_password', role='doctor'
        )

        self.doctor = DoctorProfile.objects.create(user=doctor_user)

        res = httpx.get("https://api-adresse.data.gouv.fr/search/?q=16+rue+du+paraclet+77160")
        address = res.json()["features"][0]["properties"]["label"]
        patient_user = User.objects.create_user(
            username='patient', email='patient@email.com', password='patient_password'
        )
        self.patient = PatientProfile.objects.create(
            user=patient_user,
            address=address,
            birth_date=datetime.date(year=1995, month=2, day=18)
        )

        self.doctor.patients.add(self.patient)

    def test_doctor_authentication(self):
        res = self.client.get("http://127.0.0.1:8000/")
        result = self.client.login(username=self.doctor.get_username(), password=self.doctor.user.password)
        self.assertTrue(result)

        self.client.logout()

    def test_user_authentication(self):
        result = self.client.login(
            username=self.patient.get_username(), password=self.patient.user.password
        )
        self.assertTrue(result)

        self.client.logout()