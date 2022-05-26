from django.db import models
from django.forms import Form, PasswordInput
from django.contrib.auth.models import AbstractUser


"""
All models were made in order to support offers management and point which subcontractors
are potentially interested in cooperation within indicated conditions and send proper e-mail messages to them.
"""


PROFESSIONS = [
    (-1, "Niezdefiniowano"),
    (0, "Inspektor"),
    (1, "Specjalista"),
    (2, "Zastępca dyrektora"),
    (3, "Dyrektor"),
]

COUNTRIES = [
    (-1, "Niezdefiniowano"),
    (0, "Polska"),
    (1, "Niemcy"),
    (2, "Norwegia"),
    (3, "Szwecja"),
    (4, "Dania"),
    (5, "Norwegia"),
]

REGIONS = [
    (-1, "Niezdefiniowano"),
    (2, 'Dolnośląskie'),
    (4, 'Kujawsko-Pomorskie'),
    (6, 'Lubelskie'),
    (8, 'Lubuskie'),
    (10, 'Łódzkie'),
    (12, 'Małopolskie'),
    (14, 'Mazowieckie'),
    (16, 'Opolskie'),
    (18, 'Podkarpackie'),
    (20, 'Podlaskie'),
    (22, 'Pomorskie'),
    (24, 'Śląskie'),
    (26, 'Świętokrzyskie'),
    (28, 'Warmińsko-Mazurskie'),
    (30, 'Wielkopolskie'),
    (32, 'Zachodniopomorskie'),
]

VAT_RATE = [
    (1, "Zwolniony"),
    (2, 0.00),
    (3, 0.05),
    (4, 0.08),
    (5, 0.23),
]


class User(AbstractUser):
    profession = models.IntegerField(choices=PROFESSIONS, default=-1)
    date_employed = models.DateField(null=True)


class Plant(models.Model):
    name = models.CharField(max_length=255)
    net_value = models.DecimalField(max_digits=15, decimal_places=2)
    date_begin = models.DateField()
    date_finish = models.DateField()
    related_workers = models.ManyToManyField(User)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Scope(models.Model):
    scope = models.CharField(max_length=250)

    def __str__(self):
        return self.scope


class Subcontractor(models.Model):
    name = models.CharField(max_length=255)
    mail = models.CharField(max_length=150)
    tax_connection = models.CharField(max_length=15)
    scope = models.ManyToManyField(Scope, default=-1)
    min_contract_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_contract_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class City(models.Model):
    city = models.CharField(max_length=210)
    region = models.IntegerField(choices=REGIONS, default=-1)


class Address(models.Model):
    country = models.IntegerField(choices=COUNTRIES, default=-1)
    city = models.ManyToManyField(City, default=-1)
    post_code = models.CharField(max_length=10)
    street = models.CharField(max_length=150)
    house_number = models.CharField(max_length=7)
    flat_number = models.CharField(max_length=7, null=True)
    acceptable_radius = models.IntegerField(null=True)
    subcontractor = models.ManyToManyField(Subcontractor)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT, null=True)


class Offer(models.Model):
    net_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    accepted_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True)
    vat_rate = models.IntegerField(choices=VAT_RATE, default=5)
    description = models.TextField(null=True, default=None)
    scope = models.ManyToManyField(Scope)
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owner")
    related_workers = models.ManyToManyField(User, related_name="related_workers")
    subcontractors = models.ManyToManyField(Subcontractor, related_name="subcontractors")
    winner = models.ManyToManyField(Subcontractor, related_name="winner")
    accepted_by = models.ManyToManyField(Subcontractor, related_name="accepted_by")
