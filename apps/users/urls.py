from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from apps.users.views import SignupDoctorView, CreatePatientView

app_name = "users"

urlpatterns = [
    path('signup/', SignupDoctorView.as_view(), name='doctor-signup'),
    path('patient/create', CreatePatientView.as_view(), name='add-patient'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
