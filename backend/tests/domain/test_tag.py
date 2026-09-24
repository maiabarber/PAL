import pytest

from datetime import date
from uuid import uuid4

from app.domain.Tag import Tag
from app.domain.Enums.TagStatus import TagStatus

def create_tag(**overrides):
    data = {
        "tag_id": uuid4(),
        "public_id": "K7xP9mQa4T",
        "activation_code_hash": "hashed_activation_code",
        "status": TagStatus.UNCLAIMED,
    }

    data.update(overrides)

    return Tag(**data)


def test_create_tag():
    tag_id = uuid4()

    tag = Tag(
        tag_id=tag_id,
        public_id="K7xP9mQa4T",
        activation_code_hash="hashed_activation_code",
    )

    assert tag.tag_id == tag_id
    assert tag.public_id == "K7xP9mQa4T"
    assert tag.activation_code_hash == "hashed_activation_code"
    assert tag.status == TagStatus.UNCLAIMED
    assert tag.pet_id is None
    assert tag.activation_date is None


def test_activate_tag():
    tag = create_tag()

    activation_date = date.today()

    tag.activate(activation_date)

    assert tag.status == TagStatus.ACTIVATED
    assert tag.activation_date == activation_date
    assert tag.pet_id is None


def test_only_unclaimed_tag_can_be_activated():
    tag = create_tag(
        status=TagStatus.ACTIVATED,
        activation_date=date.today(),
    )

    with pytest.raises(
        ValueError,
        match="Only an unclaimed tag can be activated"
    ):
        tag.activate(date.today())

    assert tag.status == TagStatus.ACTIVATED


def test_activation_date_cannot_be_in_future():
    tag = create_tag()

    future_date = date(
        date.today().year + 1,
        1,
        1
    )

    with pytest.raises(
        ValueError,
        match="Activation date cannot be in the future"
    ):
        tag.activate(future_date)

    assert tag.status == TagStatus.UNCLAIMED
    assert tag.activation_date is None


def test_assign_tag_to_pet():
    tag = create_tag(
        status=TagStatus.ACTIVATED,
        activation_date=date.today(),
    )

    pet_id = uuid4()

    tag.assign_to_pet(pet_id)

    assert tag.pet_id == pet_id
    assert tag.status == TagStatus.ASSIGNED


def test_unclaimed_tag_cannot_be_assigned_to_pet():
    tag = create_tag(
        status=TagStatus.UNCLAIMED
    )

    with pytest.raises(
        ValueError,
        match="Tag must be activated before it can be assigned to a pet"
    ):
        tag.assign_to_pet(uuid4())

    assert tag.pet_id is None
    assert tag.status == TagStatus.UNCLAIMED


def test_blocked_tag_cannot_be_assigned_to_pet():
    tag = create_tag(
        status=TagStatus.BLOCKED
    )

    with pytest.raises(
        ValueError,
        match="Tag must be activated before it can be assigned to a pet"
    ):
        tag.assign_to_pet(uuid4())

    assert tag.pet_id is None
    assert tag.status == TagStatus.BLOCKED


def test_pet_id_must_be_uuid_when_assigning():
    tag = create_tag(
        status=TagStatus.ACTIVATED,
        activation_date=date.today(),
    )

    with pytest.raises(
        TypeError,
        match="pet_id must be a UUID"
    ):
        tag.assign_to_pet("PET123")

    assert tag.pet_id is None
    assert tag.status == TagStatus.ACTIVATED


def test_block_tag():
    tag = create_tag(
        status=TagStatus.ASSIGNED,
        pet_id=uuid4(),
        activation_date=date.today(),
    )

    tag.block()

    assert tag.status == TagStatus.BLOCKED


def test_tag_id_must_be_uuid():
    with pytest.raises(
        TypeError,
        match="tag_id must be a UUID"
    ):
        create_tag(tag_id="123")


def test_public_id_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="public_id cannot be empty"
    ):
        create_tag(public_id="   ")


def test_activation_code_hash_cannot_be_empty():
    with pytest.raises(
        ValueError,
        match="activation_code_hash cannot be empty"
    ):
        create_tag(activation_code_hash="")


def test_status_must_be_tag_status_enum():
    with pytest.raises(
        TypeError,
        match="status must be a TagStatus value"
    ):
        create_tag(status="unclaimed")


def test_assigned_tag_must_have_pet_id():
    with pytest.raises(
        ValueError,
        match="An assigned tag must have a pet_id"
    ):
        create_tag(
            status=TagStatus.ASSIGNED,
            pet_id=None,
        )