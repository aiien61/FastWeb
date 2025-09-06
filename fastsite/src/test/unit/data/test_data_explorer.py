import os
import pytest
from model.explorer import Explorer
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from src.data.init import get_db, conn
from src.data import explorer as data

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    get_db(reset=True)
    yield
    conn.execute("DELETE FROM explorer")
    conn.commit()

@pytest.fixture()
def sample() -> Explorer:
    return Explorer(name="Indiana Jones", country="USA", description="world-famous explorer")

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.msg

def assert_duplicate(exc):
    assert exc.value.status_code == 401
    assert "already exists" in exc.value.msg

def test_create(sample):
    resp = data.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    data.create(sample)
    with pytest.raises(Duplicate) as exc:
        _ = data.create(sample)
    assert_duplicate(exc)

def test_get_one(sample):
    data.create(sample)
    resp = data.get_one_by_name(sample.name)
    assert resp == sample
    
def test_get_one_missing():
    with pytest.raises(Missing) as exc:
        _ = data.get_one_by_name("Gulliver")
    assert_missing(exc)

def test_get_all(sample):
    data.create(sample)
    resp = data.get_all()
    assert resp == [sample]

def test_modify(sample):
    data.create(sample)
    original_name: str = sample.name
    sample.country = "AUS"
    resp = data.modify(original_name, sample)
    assert resp.country == "AUS"

def test_modify_missing():
    man: Explorer = Explorer(name="Gulliver", 
                             country="UK", 
                             description="Main character of Gulliver's Travel")
    with pytest.raises(Missing) as exc:
        _ = data.modify(man.name, man)
    assert_missing(exc)

def test_delete(sample):
    data.create(sample)
    resp = data.delete(sample.name)
    assert resp is True

def test_delete_missing(sample):
    with pytest.raises(Missing) as exc:
        _ = data.delete(sample.name)
    assert_missing(exc)
