import datetime
from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from apps.users.models import User, DoctorProfile, PatientProfile


class IndexView(TemplateView):
    template_name = "core/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        if user.role == 'doctor':
            context['doctor'] = DoctorProfile.objects.get(user=user)
            self.template_name = 'dashboard/doctor/doctor-dashboard.html'
        else:
            context['patient'] = PatientProfile.objects.get(user=user)
            self.template_name = 'dashboard/patient/patient-dashboard.html'

        context['time'] = datetime.datetime.now().hour
        return context
