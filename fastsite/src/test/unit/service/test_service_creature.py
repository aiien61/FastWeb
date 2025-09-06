import os
import copy
import pytest
os.environ["CRYPTID_UNIT_TEST"] = "true"

from model.creature import Creature
from errors import Missing, Duplicate
from src.data.init import get_db, conn
from src.service import creature as service

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # SETUP: Recreate the tables on a fresh in-memory db before each test.
    get_db(reset=True)
    yield
    conn.execute("DELETE FROM creature")
    conn.commit()

@pytest.fixture
def sample() -> Creature:
    return Creature(name="Yeti",
                    aka="Abominable Snowman",
                    country="NPL",
                    area="Himalayas",
                    description="Handsom Himalayan")

def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail

def test_create(sample):
    resp = service.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    resp = service.create(sample)
    assert resp == sample
    with pytest.raises(Duplicate) as exc:
        _ = service.create(sample)
    assert_duplicate(exc)

def test_get_one(sample):
    resp = service.create(sample)
    assert resp == sample
    resp = service.get_one_by_name(sample.name)
    assert resp == sample

def test_get_one_missing(sample):
    with pytest.raises(Missing) as exc:
        _ = service.get_one_by_name(sample.name)
    assert_missing(exc)

def test_modify(sample):
    service.create(sample)

    original_name = sample.name
    sample.country = "CA"

    resp = service.modify(original_name, sample)
    assert resp.country == "CA"

def test_modify_missing():
    bob: Creature = Creature(name="bob", country="US", area="*", description="some guy", aka="??")
    with pytest.raises(Missing) as exc:
        _ = service.modify(bob.name, bob)
    assert_missing(exc)

def test_delete(sample):
    service.create(sample)
    
    resp = service.delete(sample.name)
    assert resp is True

def test_delete_missing():
    with pytest.raises(Missing) as exc:
        _ = service.delete("emu")
    assert_missing(exc)
