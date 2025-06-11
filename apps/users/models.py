from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    """
    A custom user which adds role definition

    Doctors and Patients should not access the administration interface
     aka is_staff is always at false.
    However, Doctors have more rights than Patients.

    Base attributes are:
    - username
    - email
    - first_name
    - last_name
    - password
    """
    RoleChoices = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(max_length=20, choices=RoleChoices, default='patient')

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.role == 'patient':
            patient_group, _ = Group.objects.get_or_create(name="patients")
            self.groups.add(patient_group)
        elif self.role == 'doctor':
            doctor_group, _ = Group.objects.get_or_create(name="doctors")
            self.groups.add(doctor_group)
        else:
            raise NotImplementedError('Role must be patient or doctor')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_username(self) -> str:
        return self.user.username

    def get_email(self) -> str:
        return self.user.email

    def get_role(self) -> str:
        return self.user.role

    def get_full_name(self) -> str:
        return self.user.get_full_name()

    def get_short_name(self) -> str:
        return self.user.get_short_name()


class DoctorProfile(Profile):
    patients = models.ManyToManyField('PatientProfile', related_name='doctors')

    def __str__(self) -> str:
        return f"dr {self.get_full_name()}"


class PatientProfile(Profile):
    address = models.CharField(max_length=200)
    birth_date = models.DateField()

    def __str__(self):
        return self.get_full_name()
