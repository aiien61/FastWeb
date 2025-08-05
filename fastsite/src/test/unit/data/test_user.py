import os
import pytest
from model.user import User
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import user
from data.init import get_db, conn

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    get_db(reset=True)
    yield
    conn.execute("DELETE FROM user")
    conn.execute("DELETE FROM xuser")
    conn.commit()

@pytest.fixture
def sample() -> User:
    return User(name="refield", hash="abc")

def test_create(sample):
    resp = user.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    user.create(sample)
    with pytest.raises(Duplicate):
        _ = user.create(sample)

def test_get_one(sample):
    user.create(sample)
    resp = user.get_one(sample.name)
    assert resp == sample

def test_get_one_missing():
    with pytest.raises(Missing):
        _ = user.get_one("boxturtle")

def test_modify(sample):
    user.create(sample)
    sample.hash = "new_password"
    resp = user.modify(sample.name, sample)
    assert resp.hash == "new_password"

def test_modify_missing():
    thing: User = User(name="snurfle", hash="124")
    with pytest.raises(Missing):
        _ = user.modify(thing.name, thing)

def test_delete(sample):
    user.create(sample)
    resp = user.delete(sample.name)
    with pytest.raises(Missing):
        user.get_one(sample.name)
    
    archived_user = user.get_one(sample.name, table="xuser")
    assert archived_user.name == sample.name

def test_delete_missing():
    with pytest.raises(Missing):
        _ = user.delete("non-existent-user")

