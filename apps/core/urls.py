from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
