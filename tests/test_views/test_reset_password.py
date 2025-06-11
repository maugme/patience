import re

from django.test import TestCase
from django.urls import reverse_lazy, NoReverseMatch
from django.core import mail

from apps.users.models import DoctorProfile, User


class TestPasswordResetView(TestCase):
    def setUp(self):
        doctor_user = User.objects.create_user(
            username="doctor",
            email="doctor@email.com",
            password="doctor_password",
            first_name="John",
            last_name="Doe",
            role="doctor",
        )
        self.doctor = DoctorProfile.objects.create(user=doctor_user)

    def test_reset_password_with_authenticated_user(self):
        res = self.client.post(
            reverse_lazy("users:login"),
            data={
                "username": "doctor",
                "password": "doctor_password",
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.redirect_chain[0][0], reverse_lazy("core:dashboard"))

        res = self.client.post(
            reverse_lazy("users:password-reset"), data={"email": "doctor@email.com"}
        )
        self.assertEqual(res.status_code, 403)

        res = self.client.post(reverse_lazy("users:password-reset-done"))
        self.assertEqual(res.status_code, 403)

        mail_box = mail.outbox
        self.assertFalse(mail_box)

        self.assertRaises(
            NoReverseMatch,
            self.client.post,
            reverse_lazy("users:password-reset-confirm"),
        )

        res = self.client.get(
            reverse_lazy(
                "users:password-reset-confirm",
                kwargs={
                    "uidb64": "username".encode("utf-8"),
                    "token": "token",
                },
            )
        )
        self.assertEqual(res.status_code, 403)

        res = self.client.post(reverse_lazy("users:password-reset-complete"))
        self.assertEqual(res.status_code, 403)

    def test_reset_password_without_authenticated_user(self):
        # user forgot their password and ask for resetting it
        res = self.client.get(reverse_lazy("users:password-reset"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/common/password-reset.html")

        res = self.client.post(
            reverse_lazy("users:password-reset"),
            data={"email": "doctor@email.com"},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/common/password-reset-done.html")

        # get email link
        email = mail.outbox[0]
        link_raw = re.search(r"/users/password/reset/confirm/[\S]+/", email.body)
        self.assertTrue(link_raw, "group")
        link = link_raw.group()

        res = self.client.get(link, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(link, res.redirect_chain[0][0])

        res = self.client.post(
            res.redirect_chain[0][0],
            data={
                "new_password1": "new_doctor_password",
                "new_password2": "new_doctor_password",
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/common/password-reset-complete.html")

        res = self.client.post(
            reverse_lazy("users:login"),
            data={"username": "doctor", "password": "new_doctor_password"},
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.redirect_chain[0][0], reverse_lazy('core:dashboard'))