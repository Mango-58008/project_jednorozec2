from faker import Faker
from offers_manager.models import *
from utils import *
from random import randint
import datetime


"""
This file develops all necessary tools to fill database with valid data.
Most of the data is generated by Faker.
"""


def create_users(number: int):
    """
    Creates :number: users with Faker in database and one custom, username and password both are "pjoter".
    :param number: - int; number of users to be created.
    :return: - None, used to creation, not managing data.
    """
    faker = Faker("pl_PL")
    for _ in range(number):
        random_username = generate_username()
        User.objects.create_user(username=random_username,
                                 password=faker.password(),
                                 first_name=extract_first_name(random_username),
                                 last_name=extract_last_name(random_username),
                                 is_active=True,
                                 date_joined=datetime.date(2022, 1, 1),
                                 profession=randint(0, get_max_profession_index()),
                                 date_employed=datetime.date(year=randint(2010, 2021),
                                                             month=randint(1, 12),
                                                             day=randint(1, 28)))
    # create custom user to make logging in predictable
    User.objects.create_user(username="pjoter",
                             password="pjoter",
                             first_name="pjoter",
                             last_name="pjoter",
                             is_active=True,
                             date_joined=datetime.date(2022, 1, 1),
                             profession=0,
                             date_employed=datetime.date(2022, 1, 1))


def create_plants(number: int):
    """
    Creates :number: plants with faker in database
    :param number: - int; number of plants to be created
    :return: - None, used to creation, not managing data.
    """
    faker = Faker("pl_PL")
    Faker.seed(0)
    for _ in range(number):
        users = []
        for _ in range(randint(3, 10)):
            random_user_id = randint(User.objects.first().id, User.objects.last().id)
            users.append(User.objects.get(id=random_user_id)) if random_user_id not in users else None
        date_begin = datetime.date(year=randint(2020, 2021),
                                   month=randint(1, 12),
                                   day=randint(1, 28))
        new_plant = Plant.objects.create(name=faker.catch_phrase(),
                                         net_value=randint(5000000, 500000000),
                                         date_begin=date_begin,
                                         date_finish=date_begin + datetime.timedelta(days=randint(365, 730)))
        [new_plant.related_workers.add(user) for user in users]


def create_cities(number):
    """
    Creates :number: cities with faker in database
    :param number: - int; number of cities to be created
    :return: - None, used to creation, not managing data.
    """
    # TODO: Shouldn't be more than 200. Faker only has 200 records in this method, asking for >200 cities generates infinite loop
    faker = Faker("pl_PL")
    Faker.seed(0)
    while City.objects.all().count() < number:
        city = faker.city()
        city_exists = City.objects.filter(city=city)
        if not city_exists:
            City.objects.create(city=city, region=randint(1, len(REGIONS) - 1) * 2)







def create_scopes():
    """
    Create standard building scopes in database.
    """
    Scope.objects.create(scope="Niezdefiniowano")
    Scope.objects.create(scope="Roboty ziemne")
    Scope.objects.create(scope="Roboty budowlane")
    Scope.objects.create(scope="Roboty rozbiórkowe")
    Scope.objects.create(scope="Roboty geodezyjne")
    Scope.objects.create(scope="Prace stolarskie")
    Scope.objects.create(scope="Prace tynkarskie")


def create_subcontractor(number):
    """
    Create :number: amount of subcontractors in database and one more with valid e-mail address to make manual tests.
    """
    faker = Faker("pl_PL")
    Faker.seed(0)
    for _ in range(number):
        name = faker.company()
        mail = faker.safe_email()
        tax_connection = faker.nip()
        # scope = Scope.objects.get(pk=randint(2, Scope.objects.last().id))
        scope = random.choice(list(Scope.objects.all())).id
        random_entry = randint(1, 10)
        if random_entry == 1 or random_entry == 2:
            min_contract_value = 50000
            max_contract_value = randint(min_contract_value + 150000, min_contract_value + 250000)
        elif 3 <= random_entry <= 7:
            min_contract_value = 300000
            max_contract_value = randint(min_contract_value + 350000, min_contract_value + 500000)
        else:
            min_contract_value = 800000
            max_contract_value = randint(min_contract_value + 500000, min_contract_value + 800000)
        subcontractor = Subcontractor.objects.create(name=name,
                                                     mail=mail,
                                                     tax_connection=tax_connection,
                                                     min_contract_value=min_contract_value,
                                                     max_contract_value=max_contract_value)
        subcontractor.scope.add(scope)
    # create fixed subcontractor with valid mail address
    subcontractor = Subcontractor.objects.create(name="Firma Kogucik",
                                                 mail="piotr.zaorski@mz.pl",
                                                 tax_connection=tax_connection,
                                                 min_contract_value=min_contract_value,
                                                 max_contract_value=max_contract_value)
    subcontractor.scope.add(scope)


def create_address(number):
    """
    Create :number: amount of addresses in database.
    """
    faker = Faker("pl_PL")
    Faker.seed(0)
    for _ in range(number):
        country = 0
        city = City.objects.get(pk=randint(City.objects.first().id, City.objects.last().id))
        # city = random.choice(list(City.objects.all())).id
        post_code = faker.postcode()
        street = faker.street_name()
        house_number = randint(1, 700)
        flat_number_manager = randint(1, 10)
        if flat_number_manager < 7:
            flat_number = randint(1, 120)
        else:
            flat_number = None
        acceptable_radius = None
        subcontractor = Subcontractor.objects.get(pk=randint(Subcontractor.objects.first().id, Subcontractor.objects.last().id))
        # subcontractor = random.choice(list(Subcontractor.objects.all())).id
        plant = None
        address = Address.objects.create(country=country,
                                         post_code=post_code,
                                         street=street,
                                         house_number=house_number,
                                         flat_number=flat_number,
                                         acceptable_radius=acceptable_radius,
                                         plant=plant)
        address.subcontractor.add(subcontractor)
        address.city.add(city)

    counter = 1
    for _ in range(Plant.objects.count()):
        country = 0
        city = City.objects.get(pk=randint(City.objects.first().id, City.objects.last().id))
        # city = random.choice(list(City.objects.all())).id
        post_code = faker.postcode()
        street = faker.street_name()
        house_number = randint(1, 700)
        flat_number_manager = randint(1, 10)
        if flat_number_manager < 7:
            flat_number = randint(1, 120)
        else:
            flat_number = None
        acceptable_radius = None
        # plant = Plant.objects.get(pk=counter)
        counter += 1
        address = Address.objects.create(country=country,
                                         post_code=post_code,
                                         street=street,
                                         house_number=house_number,
                                         flat_number=flat_number,
                                         acceptable_radius=acceptable_radius,
                                         plant=plant)
        address.city.add(city)


def create_offers(number):
    """
    Create :number: amount of offers in database.
    """
    for _ in range(number):
        random_entry = randint(1, 10)
        if random_entry == 1 or random_entry == 2:
            net_value = randint(50000, 300000)
        elif 3 <= random_entry <= 7:
            net_value = randint(30000, 800000)
        else:
            net_value = randint(800000, 1600000)
        # vat_rate default 0.23
        description = _
        # scope = Scope.objects.get(pk=randint(2, Scope.objects.last().id))
        plant = Plant.objects.get(pk=randint(Plant.objects.first().id, Plant.objects.last().id))
        owner = User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))
        scope = random.choice(list(Scope.objects.all())).id
        # plant = random.choice(list(Plant.objects.all())).id
        # owner = random.choice(list(User.objects.all())).id
        users = [owner.id]
        for _ in range(randint(3, 10)):
            random_user_id = randint(User.objects.first().id, User.objects.last().id)
            # random_user_id = random.choice(list(User.objects.all())).id
            users.append(User.objects.get(id=random_user_id)) if random_user_id not in users else None
        offer = Offer.objects.create(net_value=net_value,
                                     plant=plant,
                                     description=description,
                                     owner=owner)
        offer.scope.add(scope)
        [offer.related_workers.add(user) for user in users]
