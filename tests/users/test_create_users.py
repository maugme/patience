import datetime

from django.test import TestCase, tag
from apps.users.models import User, DoctorProfile, PatientProfile


@tag("unit_test")
class TestCreateUser(TestCase):
    def test_create_doctor_profile(self):
        doctor_user = User.objects.create(
            username="doctor",
            email="doctor@email.com",
            password="doctor_password",
            first_name="John",
            last_name="Doe",
            role="doctor",
        )

        doctor = DoctorProfile.objects.create(user=doctor_user)

        self.assertTrue(doctor.get_role())
        self.assertEqual(doctor.user.role, "doctor")

        self.assertIn("Dr", str(doctor))

        self.assertTrue(doctor.get_username())

        self.assertTrue(doctor.get_email())

        self.assertTrue(doctor.get_full_name())

        self.assertTrue(doctor.get_short_name())

    def test_create_patient_profile(self):
        patient_user = User.objects.create(
            username="patient",
            email="patient@email.com",
            password="patient_password",
            first_name="Jane",
            last_name="Doe",
            role="patient",
        )

        patient = PatientProfile.objects.create(
            user=patient_user,
            address="16 Rue du Paraclet 77160 Provins",
            birth_date=datetime.datetime(year=1995, month=2, day=18)
        )

        self.assertTrue(patient.get_role())
        self.assertEqual(patient.user.role, "patient")

        self.assertNotIn("Dr", str(patient))

        self.assertTrue(patient.get_username())

        self.assertTrue(patient.get_email())

        self.assertTrue(patient.get_full_name())

        self.assertTrue(patient.get_short_name())
