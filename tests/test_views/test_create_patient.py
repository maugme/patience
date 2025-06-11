import datetime
import re

from django.core import mail
from django.test import TestCase, tag, Client
from django.urls import reverse_lazy

from apps.users.models import User, PatientProfile, DoctorProfile


@tag("integration_test")
class TestCreatePatient(TestCase):
    def setUp(self):
        # create a doctor
        doctor_user = User.objects.create_user(
            username="doctor",
            email="doctor@email.com",
            password="doctor_password",
            first_name="John",
            last_name="Doe",
            role="doctor",
        )
        self.doctor = DoctorProfile.objects.create(user=doctor_user)

        # create a patient
        patient_user = User.objects.create_user(
            username="patient",
            email="patient@email.com",
            first_name="Jack",
            last_name="Doe",
            password="patient_password",
            role="patient",
        )

        self.patient = PatientProfile.objects.create(
            **{
                "user": patient_user,
                "birth_date": datetime.datetime(year=1999, month=1, day=1),
                "address": "16 Rue du Paraclet 77160 Provins",
            }
        )

        # store patient data used in forms for convenience
        self.patient_new_data = {
            "username": "patient_new",
            "email": "patient@email.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "birth_date": "18/02/1995",
            "address": "16 Rue du Paraclet 77160 Provins",
        }

    def test_doctor_add_patient(self):
        # log the doctor user in
        res = self.client.post(
            reverse_lazy("users:login"),
            data={
                "username": self.doctor.get_username(),
                "password": "doctor_password",
            },
            follow=True,
        )

        # should be valid
        self.assertEqual(res.status_code, 200)

        # create a patient with a doctor
        res = self.client.post(
            reverse_lazy("users:create-patient"),
            data=self.patient_new_data,
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "core/dashboard/doctor/doctor-dashboard.html")

        # the patient must get the link in its mail and follow the password creation process
        patient_client = Client()
        email = mail.outbox[0]

        # retrieve the link in the mail
        raw_link = re.search(r"/users/patient/password/init/confirm/[\S]+/", email.body)
        self.assertTrue(hasattr(raw_link, "group"))

        link = raw_link.group()

        # access the link
        res = patient_client.get(link, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.request.get("PATH_INFO"), link)

        # get the new password form
        next_link = res.request.get("PATH_INFO")

        # set the new password
        res = patient_client.post(
            next_link,
            data={
                "new_password1": "patient_password",
                "new_password2": "patient_password",
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.request.get("PATH_INFO"), reverse_lazy("users:password-reset-complete")
        )

        # test connection with the new patient
        res = patient_client.post(
            reverse_lazy("users:login"),
            data={
                "username": self.patient_new_data["username"],
                "password": "patient_password",
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request.get("PATH_INFO"), reverse_lazy("core:dashboard"))

    def test_anonymous_add_patient(self):
        # try to create a patient without being connected
        res = self.client.post(
            reverse_lazy("users:create-patient"), data=self.patient_new_data
        )

        # should return a 403 error
        self.assertEqual(res.status_code, 403)

    def test_patient_add_patient(self):
        # try to create a patient without being connected
        res = self.client.post(
            reverse_lazy("users:login"),
            data={
                "username": self.patient.get_username(),
                "password": "patient_password",
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "core/dashboard/patient/patient-dashboard.html")
        res = self.client.post(
            reverse_lazy("users:create-patient"), data=self.patient_new_data
        )

        # should return a 403 error
        self.assertEqual(res.status_code, 403)
