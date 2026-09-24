from datetime import date
from uuid import UUID

from .Enums.TagStatus import TagStatus


class Tag:

    def __init__(
        self,
        tag_id: UUID, ## Represents the unique identifier for the tag. It is expected to be a UUID (Universally Unique Identifier) object.
        public_id: str, ## Represents the public identifier for the tag. It is expected to be a non-empty string that uniquely identifies the tag in a public context.
        activation_code_hash: str, ## Represents the hash of the activation code for the tag. It is expected to be a non-empty string.
        status: TagStatus = TagStatus.UNCLAIMED,
        pet_id: UUID | None = None,
        activation_date: date | None = None,
    ):
        if not isinstance(tag_id, UUID):
            raise TypeError("tag_id must be a UUID.")

        if not public_id or not public_id.strip():
            raise ValueError("public_id cannot be empty.")

        if not activation_code_hash or not activation_code_hash.strip():
            raise ValueError("activation_code_hash cannot be empty.")

        if not isinstance(status, TagStatus):
            raise TypeError("status must be a TagStatus value.")

        if status == TagStatus.ASSIGNED and pet_id is None:
            raise ValueError("An assigned tag must have a pet_id.")

        self.tag_id = tag_id
        self.public_id = public_id.strip()
        self.activation_code_hash = activation_code_hash
        self.status = status
        self.pet_id = pet_id
        self.activation_date = activation_date

    def activate(self, activation_date: date):
        if self.status != TagStatus.UNCLAIMED:
            raise ValueError("Only an unclaimed tag can be activated.")

        if activation_date > date.today():
            raise ValueError("Activation date cannot be in the future.")

        self.status = TagStatus.ACTIVATED
        self.activation_date = activation_date

    def assign_to_pet(self, pet_id: UUID):
        if self.status != TagStatus.ACTIVATED:
            raise ValueError(
                "Tag must be activated before it can be assigned to a pet."
            )

        if not isinstance(pet_id, UUID):
            raise TypeError("pet_id must be a UUID.")

        self.pet_id = pet_id
        self.status = TagStatus.ASSIGNED

    def block(self):
        self.status = TagStatus.BLOCKED