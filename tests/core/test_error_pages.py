from django.contrib.admindocs.views import ViewDetailView
from django.core.exceptions import PermissionDenied, SuspiciousOperation, ImproperlyConfigured
from django.http import Http404
from django.test import TestCase, Client, override_settings
from django.urls import path
from django.views import defaults

def response_400(request):
    raise SuspiciousOperation

def response_403(request):
    raise PermissionDenied

def response_404(request):
    raise Http404

def response_500(request):
    raise ImproperlyConfigured

urlpatterns = [
    path("400/", response_400),
    path("403/", response_403),
    path("404/", response_404),
    path("500/", response_500),
]


@override_settings(ROOT_URLCONF=__name__, DEBUG=False)
class TestErrorPage(TestCase):
    def test_404_error(self):
        response = self.client.get("/404/",)
        self.assertTemplateUsed(response, template_name="404.html")
        self.assertContains(response, "Pas de page trouvée", status_code=404)

    def test_500_error(self):
        with self.assertRaises(ImproperlyConfigured):
            response = self.client.get("/500/")
            self.assertTemplateUsed(response, template_name="500.html")
            self.assertContains(response, "Problème côté serveur. Réessayer plus tard.")


    def test_403_error(self):
        response = self.client.get("/403/")
        self.assertTemplateUsed(response, template_name="403.html")
        self.assertContains(response, "Vous n'avez pas la permission d'accéder à ou de modifier cette ressource.", status_code=403)


    def test_400_error(self):
        response = self.client.get("/400/")
        self.assertTemplateUsed(response, template_name="400.html")
        self.assertContains(response, "La demande d'accès à ou de modification de cette ressource est mal formulée", status_code=400)
