import os
import pytest
from model.user import User
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from src.data import user
from src.data.init import get_db, conn

# CRITICAL FOR TESTING: The autouse=True fixture is the key to test isolation.
# It guarantees that every single test in this file runs with a clean, empty database.
@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # SETUP: Recreate the tables on a fresh in-memory db before each test.
    get_db(reset=True)
    yield

    # TEARDOWN: Clean all data after each test to prevent state leakage.
    conn.execute("DELETE FROM user")
    conn.execute("DELETE FROM xuser")
    conn.commit()

@pytest.fixture
def sample() -> User:
    return User(name="refield", hash="abc")

def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail

def test_create(sample):
    resp = user.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    # NOTE: This is the correct pattern for self-contained tests.
    # 1. Arrange: Create the user so it exists.
    user.create(sample)

    # 2. Act & Assert: Check that creating it again raises the expected error.
    with pytest.raises(Duplicate) as exc:
        _ = user.create(sample)
    assert_duplicate(exc)

def test_get_one(sample):
    user.create(sample)
    resp = user.get_one_by_name(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing) as exc:
        _ = user.get_one_by_name("boxturtle")
    assert_missing(exc)

def test_modify(sample):
    user.create(sample)
    sample.hash = "new_password"
    resp = user.modify(sample.name, sample)
    assert resp.hash == "new_password"

def test_modify_missing():
    thing: User = User(name="snurfle", hash="124")
    with pytest.raises(Missing) as exc:
        _ = user.modify(thing.name, thing)
    assert_missing(exc)

def test_delete(sample):
    user.create(sample)
    resp = user.delete(sample.name)
    with pytest.raises(Missing):
        user.get_one_by_name(sample.name)
    
    archived_user = user.get_one_by_name(sample.name, table="xuser")
    assert archived_user.name == sample.name

def test_delete_missing():
    with pytest.raises(Missing) as exc:
        _ = user.delete("non-existent-user")
    assert_missing(exc)
