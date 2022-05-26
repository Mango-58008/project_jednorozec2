from django.core.management.base import BaseCommand, CommandError
from .functions import *
from offers_manager.models import User


"""
This module is helpful to test offers_manager application on other appliances.
Just type "python manage.py fill_database" in the terminal.
Merged all commands into one because there is many relations in model, so order is constrained.
"""


class Command(BaseCommand):
    help = "Fill database with valid data"

    def handle(self, *args, **options):
        user_count = User.objects.all().count()
        if user_count > 10:
            raise CommandError("Database if already filled")
        create_users(50)
        self.stdout.write(self.style.SUCCESS("Filled database successfully."))
