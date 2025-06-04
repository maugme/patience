from typing import override
from django.contrib.auth import authenticate
from django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin, FormMixin

from apps.users.forms import DoctorSignupForm, CreatePatientForm
from apps.users.models import DoctorProfile, PatientProfile


class SignupDoctorView(CreateView):
    form_class = DoctorSignupForm
    template_name = "users/doctor-signup.html"
    success_url = "users/login/"


class CreatePatientView(CreateView):
    form_class = CreatePatientForm
    template_name = "users/create-patient.html"
    success_url = "/dashboard/"

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = DoctorProfile.objects.get(user_id=self.request.user.id)
        patient = PatientProfile.objects.get(user_id=self.object.id)
        doctor.patients.add(patient)
        doctor.save()
        return  response