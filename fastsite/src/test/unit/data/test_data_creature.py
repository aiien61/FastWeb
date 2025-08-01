import os
import pytest
from model.creature import Creature
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature
from data.init import get_db, conn

# This fixture provides a clean database for EVERY test.
@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # Setup: Create tables
    get_db(reset=True)
    yield

    # Teardown: Clean up data after the test is done
    conn.execute("DELETE FROM creature")
    conn.commit()

@pytest.fixture
def sample() -> Creature:
    return Creature(name="Yeti", 
                    aka="Abominable Snowman",
                    country="NPL",
                    area="Himalayas",
                    description="Hirsute Himalayan")

def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    # create the creature so it exists in the db
    creature.create(sample)

    # test that creating it again raises a duplicate error
    with pytest.raises(Duplicate):
        _ = creature.create(sample)

def test_get_one(sample):
    creature.create(sample)
    resp = creature.get_one(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")

def test_modify(sample):
    creature.create(sample)
    creature.area = "Seasame Street"
    resp = creature.modify(sample)
    assert resp == sample

def test_delete(sample):
    # Create the creature to be deleted
    creature.create(sample)
    # delete it by name
    resp = creature.delete(sample.name)
    assert resp is True

def test_delete_missing():
    with pytest.raises(Missing):
        _ = creature.delete("non-existent creature")
