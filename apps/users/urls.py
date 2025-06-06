from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.urls import path, reverse_lazy

from apps.users.views import (
    SignupDoctorView,
    CreatePatientView,
)

app_name = "users"

urlpatterns = [
    # doctor creation
    path("doctor/signup/", SignupDoctorView.as_view(), name="create-doctor"),
    # patient auth management
    path("patient/create/", CreatePatientView.as_view(), name="create-patient"),
    path(
        "patient/password/init/confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/patient/init-password-confirm-view.html",
            success_url=reverse_lazy("users:reset-password-complete"),
        ),
        name="init-password-confirm",
    ),
    path(
        "password/init/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/patient/init-password-complete.html"
        ),
        name="init-password-complete",
    ),
    path(
        "password/init/done/",
        PasswordResetDoneView.as_view(
            template_name="users/patient/init-password-done-view.html"
        ),
        name="init-password-done",
    ),
    # all user auth management
    path(
        "login/", LoginView.as_view(template_name="users/all/login.html"), name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="users/all/logout.html"),
        name="logout",
    ),
    path(
        "password/reset/",
        PasswordResetView.as_view(
            template_name="users/all/reset-password.html",
            email_template_name="users/email/reset-password-email.html",
            subject_template_name="users/email/reset-password-subject.txt",
            success_url=reverse_lazy("users:reset-password-done"),
        ),
        name="reset-password",
    ),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/all/reset-password-done-view.html"
        ),
        name="reset-password-done",
    ),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/all/reset-password-confirm-view.html",
            success_url=reverse_lazy("users:reset-password-complete"),
        ),
        name="reset-password-confirm",
    ),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/all/reset-password-complete.html"
        ),
        name="reset-password-complete",
    ),
]
