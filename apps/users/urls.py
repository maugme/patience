from django.urls import path, reverse_lazy

from apps.users.views import (
    SignupDoctorView,
    CreatePatientView,
    PatientPasswordInitConfirmView,
    PatientPasswordInitCompleteView,
    PatientPasswordInitDoneView,
    UserLoginView,
    UserLogoutView,
    UserPasswordResetView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
)

app_name = "users"

urlpatterns = [
    # doctor creation
    path("doctor/signup/", SignupDoctorView.as_view(), name="create-doctor"),
    # patient auth management
    path("patient/create/", CreatePatientView.as_view(), name="create-patient"),
    path(
        "patient/password/init/confirm/<str:uidb64>/<str:token>/",
        PatientPasswordInitConfirmView.as_view(),
        name="password-init-confirm",
    ),
    path(
        "password/init/complete/",
        PatientPasswordInitCompleteView.as_view(),
        name="password-init-complete",
    ),
    path(
        "password/init/done/",
        PatientPasswordInitDoneView.as_view(),
        name="password-init-done",
    ),
    # all user auth management
    path(
        "login/", UserLoginView.as_view(), name="login"
    ),
    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),
    path(
        "password/reset/",
        UserPasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/done/",
        UserPasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password/reset/complete/",
        UserPasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
]
