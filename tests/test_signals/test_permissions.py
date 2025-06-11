from django.contrib.auth.models import Group
from django.test import TestCase, tag


@tag("unit_test")
class TestPermissionsView(TestCase):
    def test_doctor_permissions(self):
        doctor_group = Group.objects.get(name="doctors")
        permissions = doctor_group.permissions.values_list("codename", flat=True)
        self.assertEqual(
            tuple(permissions),
            ("add_patientprofile", "view_patientprofile"),
        )

    def test_patient_permissions(self):
        patient_group = Group.objects.get(name="patients")
        permissions = patient_group.permissions.values_list("codename", flat=True)
        self.assertEqual(list(permissions), [])