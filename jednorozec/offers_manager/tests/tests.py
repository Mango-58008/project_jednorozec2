import datetime
import pytest
from offers_manager.models import *
from offers_manager.management.commands.common_parts import create_plants
from django.test import TestCase


"""
Automation tests. This module is pretty poor - designers had some deadlines.
"""


@pytest.mark.django_db
def test_home_page(client):
    response = client.get("/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register(client):
    response = client.get("/zarejestruj/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
class Tests(TestCase):
    def test_log_in(self):
        response = self.client.get("/zaloguj/", {}, format='json')
        assert response.status_code == 200
        response = self.client.post("/zaloguj/",
                                    {"username": "pjoter",
                                     "password": "pjoter"},
                                    format='json')
        assert response.status_code == 200
        session = self.client.session
        session["username"] = "pjoter"
        session.save()
        self.assertEqual(self.client.session["username"], "pjoter")

    def test_log_out(self):
        session = self.client.session
        session.clear()
        response = self.client.post("/wyloguj/", {}, format='json')
        assert response.status_code == 200

    def test_new_plant(self):
        session = self.client.session
        session["username"] = "pjoter"
        session.save()
        response = self.client.get("/dodaj_budowe/", {}, format='json')
        assert response.status_code == 200
        response = self.client.get("/dodaj_budowe/",
                                   {"plant_name": "testowa",
                                    "net_value": 555,
                                    "date_begin": datetime.date(2021, 1, 1),
                                    "date_finish": datetime.date(2022, 1, 1),
                                    "country": 1,
                                    "city": "Warszawa",
                                    "post_code": "44-111",
                                    "street": "Wolności",
                                    "house_number": 1,
                                    "flat_number": 1},
                                   format='json')
        assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard(client):
    response = client.get("/dashboard/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_new_offer(client):
    response = client.get("/dodaj_oferte/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_plant(client, set_up):
    response = client.get(f"/edytuj_budowe/{Plant.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_offer(client, set_up):
    response = client.get(f"/edytuj_oferte/{Offer.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_plant_new_workers(client, set_up):
    response = client.get(f"/edytuj_budowe/{Plant.objects.first().id}/dodaj_pracownikow/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_offer_new_workers(client, set_up):
    response = client.get(f"/edytuj_oferte/{Offer.objects.first().id}/dodaj_pracownikow/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_close_plant(client, set_up):
    response = client.get(f"/zamknij_budowe/{Plant.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_close_offer(client, set_up):
    response = client.get(f"/zamknij_oferte/{Offer.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_offers(client):
    response = client.get("/oferty/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_send_emails(client, set_up):
    response = client.get(f"/wyslij_zapytania/{Offer.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_subcontractors(client, set_up):
    response = client.get(f"/dodaj_podwykonawcow/{Offer.objects.first().id}/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_subcontractors(client):
    response = client.get("/podwykonawcy/", {}, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_subcontractor(client, set_up):
    response = client.get(f"/podwykonawca/{Subcontractor.objects.first().id}/", {}, format='json')
    assert response.status_code == 200
