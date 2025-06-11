import datetime

import httpx
from django.test import TestCase, Client, tag
from django.urls import reverse_lazy

from apps.users.models import User, DoctorProfile, PatientProfile


@tag('integration_test')
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

    def test_doctor_login(self):
        result = self.client.login(username=self.doctor.get_username(), password='doctor_password')
        self.assertTrue(result)

        self.client.logout()

    def test_patient_login(self):
        result = self.client.login(
            username=self.patient.get_username(), password="patient_password"
        )
        self.assertTrue(result)
        self.client.logout()

    def test_dashboard_access(self):
        for user in (self.doctor, self.patient):
            response = self.client.post(
                reverse_lazy("users:login"),
                data={"username": user.get_username(), "password": f"{user.get_role()}_password"}
            )
            self.assertRedirects(
                response, reverse_lazy("core:dashboard"), status_code=302, target_status_code=200
            )

            # disconnect user and test whether it can access the dashboard
            self.client.post(reverse_lazy("users:logout"))
            response = self.client.get(reverse_lazy("core:dashboard"))
            self.assertRedirects(response, '/users/login/?next=/dashboard/')

    def test_bad_credentials(self):
        res = self.client.post(
            reverse_lazy("users:login"), data={"username": "doctor", "password": "<PASSWORD>"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Saisissez un nom d’utilisateur et un mot de passe valides")
        self.assertFalse(hasattr(res, 'redirect_chain'))

        res = self.client.post(
            reverse_lazy("users:login"), data={"username": "bad_doctor", "password": "doctor_password"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Saisissez un nom d’utilisateur et un mot de passe valides")
        self.assertFalse(hasattr(res, 'redirect_chain'))
