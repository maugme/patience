from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def update_permissions(sender: AppConfig, **kwargs):
    if sender.label == 'users':
        # doctor permissions
        # TODO: add logs here
        doctor_group, _ = Group.objects.get_or_create(name="doctors")

        doctor_permissions = Permission.objects.filter(codename__in=[
            'add_patientprofile',
            'view_patientprofile',
        ]).all()
        doctor_group.permissions.set(doctor_permissions)

        # patient permissions
        patient_group, _ = Group.objects.get_or_create(name="patients")
