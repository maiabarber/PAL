import pytest

from datetime import date
from uuid import uuid4

from app.domain.Pet import Pet
from app.domain.Enums.Gender import Gender
from app.domain.Enums.Species import Species

##this method creates a pet object with default values, which can be overridden by passing keyword arguments. 
# It is used in the test cases to create pet objects for testing purposes.
def create_pet(**overrides):
    data = {
        "pet_id": uuid4(),
        "owner_id": uuid4(),
        "name": "Buddy",
        "species": Species.DOG,
        "birth_date": date(2020, 5, 15),
        "gender": Gender.MALE,
    }

    data.update(overrides)

    return Pet(**data)


def test_create_pet():
    pet_id = uuid4()
    owner_id = uuid4()

    pet = Pet(
        pet_id=pet_id,
        owner_id=owner_id,
        name="Buddy",
        species=Species.DOG,
        birth_date=date(2020, 5, 15),
        gender=Gender.MALE,
    )

    assert pet.pet_id == pet_id
    assert pet.owner_id == owner_id
    assert pet.name == "Buddy"
    assert pet.species == Species.DOG
    assert pet.birth_date == date(2020, 5, 15)
    assert pet.gender == Gender.MALE
    assert pet.photo_url is None
    assert pet.microchip_number is None
    assert pet.lost_mode is False
    assert pet.public_notes is None


def test_calculate_age():
    birth_date = date(2020, 5, 15)

    pet = create_pet(birth_date=birth_date)

    expected_age = date.today().year - birth_date.year

    if (date.today().month, date.today().day) < (
        birth_date.month,
        birth_date.day
    ):
        expected_age -= 1

    assert pet.calculate_age() == expected_age


def test_enable_lost_mode():
    pet = create_pet(lost_mode=False)

    pet.enable_lost_mode()

    assert pet.lost_mode is True


def test_disable_lost_mode():
    pet = create_pet(lost_mode=True)

    pet.disable_lost_mode()

    assert pet.lost_mode is False


def test_pet_name_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="Pet name cannot be empty"
    ):
        create_pet(name="   ")


def test_pet_name_must_contain_letters_only():
    with pytest.raises(
        ValueError,
        match="Pet name must contain letters only"
    ):
        create_pet(name="Buddy123")


def test_pet_name_with_letters_is_valid():
    pet = create_pet(name="Buddy")

    assert pet.name == "Buddy"


def test_hebrew_pet_name_is_valid():
    pet = create_pet(name="לונה")

    assert pet.name == "לונה"


def test_pet_name_is_trimmed():
    pet = create_pet(name="  Buddy  ")

    assert pet.name == "Buddy"


def test_birth_date_cannot_be_in_future():
    future_date = date(
        date.today().year + 1,
        1,
        1
    )

    with pytest.raises(
        ValueError,
        match="Birth date cannot be in the future"
    ):
        create_pet(birth_date=future_date)


def test_rename_pet():
    pet = create_pet(name="Buddy")

    pet.rename("Luna")

    assert pet.name == "Luna"


def test_rename_pet_with_invalid_name():
    pet = create_pet()

    with pytest.raises(
        ValueError,
        match="Pet name must contain letters only"
    ):
        pet.rename("Luna123")

    assert pet.name == "Buddy"


def test_pet_id_must_be_uuid():
    with pytest.raises(
        TypeError,
        match="pet_id must be a UUID"
    ):
        create_pet(pet_id="123")


def test_owner_id_must_be_uuid():
    with pytest.raises(
        TypeError,
        match="owner_id must be a UUID"
    ):
        create_pet(owner_id="123")


def test_species_must_be_species_enum():
    with pytest.raises(
        TypeError,
        match="species must be a Species value"
    ):
        create_pet(species="dog")


def test_gender_must_be_gender_enum():
    with pytest.raises(
        TypeError,
        match="gender must be a Gender value"
    ):
        create_pet(gender="male")