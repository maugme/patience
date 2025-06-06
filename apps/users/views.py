from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView
from pre_commit.util import force_bytes

from apps.users.forms import DoctorSignupForm, CreatePatientForm
from apps.users.models import DoctorProfile, PatientProfile
from django.contrib.auth.tokens import default_token_generator


class SignupDoctorView(CreateView):
    form_class = DoctorSignupForm
    template_name = "users/doctor/create-doctor.html"
    success_url = reverse_lazy('users:login')


class CreatePatientView(LoginRequiredMixin, CreateView):
    form_class = CreatePatientForm
    template_name = "users/patient/create-patient.html"
    success_url = reverse_lazy("users:password-init-done")

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = DoctorProfile.objects.get(user_id=self.request.user.id)
        patient = PatientProfile.objects.get(user_id=self.object.id)
        doctor.patients.add(patient)
        doctor.save()

        # send email to user
        context = {
            "user": patient,
            "doctor": doctor,
            "protocol": "http",
            "domain": get_current_site(self.request),
            "uid": urlsafe_base64_encode(force_bytes(str(self.object.pk))),
            "token": default_token_generator.make_token(self.object),
        }

        send_mail(
            subject=render_to_string("users/email/create-patient-subject.txt", context=context),
            message=render_to_string("users/email/create-patient-email.html", context=context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[patient.get_email()],
            fail_silently=False
        )
        return response


class PatientPasswordInitConfirmView(PasswordResetConfirmView):
    template_name = "users/patient/password-init-confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")


class PatientPasswordInitCompleteView(PasswordResetCompleteView):
    template_name="users/patient/password-init-complete.html"


class PatientPasswordInitDoneView(PasswordResetCompleteView):
    template_name="users/patient/password-init-done.html"


class UserLoginView(LoginView):
    template_name="users/common/login.html"


class UserLogoutView(LogoutView):
    template_name="users/common/logout.html"


class UserPasswordResetView(PasswordResetView):
    template_name = "users/common/password-reset.html"
    email_template_name = "users/email/password-reset-email.html"
    subject_template_name = "users/email/password-reset-subject.txt"
    success_url = reverse_lazy("users:password-reset-done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name="users/common/password-reset-done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/common/password-reset-confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/common/password-reset-complete.html"
