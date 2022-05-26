import os
import sys
import pytest
from rest_framework.test import APIClient
from offers_manager.management.commands.common_parts import *


sys.path.append(os.path.dirname(__file__))


"""
This file has fixtures. Fixtures are repeatably used simulation tools.
"""


@pytest.fixture
def client():
    """
    Returns APIClient for web explorer
    """
    client = APIClient()
    return client


@pytest.fixture
def set_up():
    """
    Creates valid database records in order to work properly on data.
    """
    create_scopes()
    create_cities(2)
    create_users(10)
    create_plants(15)
    create_subcontractor(3)
    create_address(15)
    create_offers(3)
