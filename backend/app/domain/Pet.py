from datetime import date
from uuid import UUID

from .Enums.Species import Species
from .Enums.Gender import Gender


class Pet:

    def __init__(
        self,
        pet_id: UUID,
        owner_id: UUID,
        name: str,
        species: Species,
        birth_date: date,
        gender: Gender,
        photo_url: str | None = None,
        microchip_number: str | None = None,
        lost_mode: bool = False,
        public_notes: str | None = None,
    ):
        name = self._validate_name(name)

        if birth_date > date.today():
            raise ValueError("Birth date cannot be in the future.")

        if not isinstance(pet_id, UUID):
            raise TypeError("pet_id must be a UUID.")

        if not isinstance(owner_id, UUID):
            raise TypeError("owner_id must be a UUID.")

        if not isinstance(species, Species):
            raise TypeError("species must be a Species value.")

        if not isinstance(gender, Gender):
            raise TypeError("gender must be a Gender value.")

        self.pet_id = pet_id
        self.owner_id = owner_id
        self.name = name
        self.species = species
        self.birth_date = birth_date
        self.gender = gender
        self.photo_url = photo_url
        self.microchip_number = microchip_number
        self.lost_mode = lost_mode
        self.public_notes = public_notes

    @staticmethod
    def _validate_name(name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("Pet name cannot be empty.")

        if not name.isalpha():
            raise ValueError("Pet name must contain letters only.")

        return name

    def calculate_age(self) -> int:
        today = date.today()

        age = today.year - self.birth_date.year

        if (today.month, today.day) < (
            self.birth_date.month,
            self.birth_date.day
        ):
            age -= 1

        return age

    def rename(self, new_name: str):
        self.name = self._validate_name(new_name)

    def enable_lost_mode(self):
        self.lost_mode = True

    def disable_lost_mode(self):
        self.lost_mode = False