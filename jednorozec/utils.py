from faker import Factory
from offers_manager.models import *


"""
This module contains some basic functions that are being used in views and BaseCommand.
"""


def replace_polish_characters(string):
    """
    My application won't allow polish characters in username. This function replaces it to its equivalents.
    This function is meant to work only with faker.
    """
    string = string.lower()
    forbidden = ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ż", "ź"]
    allowed = ["a", "c", "e", "l", "n", "o", "s", "z", "z"]
    for char in string:
        if char in forbidden:
            string = string.replace(char, allowed[forbidden.index(char)])
    return string


def generate_username():
    """
    Generate username, which consists of first name, last name and a proper domain.
    """
    fake = Factory.create("pl_PL")
    return replace_polish_characters(fake.first_name()) + "." + replace_polish_characters(fake.last_name()) + "@mz.pl"


def extract_first_name(username):
    """
    Get first name out of username.
    """
    return username[:username.find(".")].capitalize()


def extract_last_name(username):
    """
    Get last name out of username.
    """
    return username[username.find(".") + 1:username.find("@")].capitalize()


def extract_full_name(username):
    """
    Get full name out of username.
    """
    return extract_first_name(username) + " " + extract_last_name(username)


def get_max_profession_index():
    max_number = 0
    for profession in PROFESSIONS:
        max_number = profession[0] if profession[0] > max_number else 0
    return max_number
