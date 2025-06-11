import datetime

from django.test import TestCase, tag

from apps.users.models import User, DoctorProfile, PatientProfile


@tag("unit_test")
class TestProfileModel(TestCase):
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
        self.assertEqual(f"dr {doctor.get_full_name()}", str(doctor))

        self.assertTrue(hasattr(doctor_user, "doctorprofile"))
        self.assertEqual(doctor.get_username(), doctor.user.username)
        self.assertEqual(doctor.get_email(), doctor.user.email)
        self.assertEqual(
            doctor.get_full_name(), doctor.user.first_name + " " + doctor.user.last_name
        )
        self.assertEqual(doctor.get_short_name(), doctor.user.first_name)

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
            birth_date=datetime.datetime(year=1995, month=2, day=18),
        )

        self.assertTrue(patient.get_role())
        self.assertEqual(patient.user.role, "patient")
        self.assertEqual(patient.get_full_name(), str(patient))

        self.assertTrue(hasattr(patient_user, "patientprofile"))
        self.assertEqual(patient.get_username(), patient.user.username)
        self.assertEqual(patient.get_email(), patient.user.email)
        self.assertEqual(
            patient.get_full_name(),
            patient.user.first_name + " " + patient.user.last_name,
        )
        self.assertEqual(patient.get_short_name(), patient.user.first_name)
