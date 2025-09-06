import os
import pytest
os.environ["CRYPTID_UNIT_TEST"] = "true"

from model.explorer import Explorer
from src.service import explorer as service
from src.data.init import get_db, conn
from errors import Missing, Duplicate

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    get_db()
    yield
    conn.execute("DELETE FROM explorer")
    conn.commit()

@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Claude Hande",
                    country="FR",
                    description="Scarce during full moons")

@pytest.fixture
def fakes() -> list[Explorer]:
    return service.get_all()

def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.msg

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.msg

def test_create(sample):
    resp = service.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    service.create(sample)
    with pytest.raises(Duplicate) as exc:
        _ = service.create(sample)
    assert_duplicate(exc)

def test_get_one(sample):
    service.create(sample)
    resp = service.get_one_by_name(sample.name)
    assert resp == sample

def test_get_one_missing(sample):
    with pytest.raises(Missing) as exc:
        _ = service.get_one_by_name(sample.name)
    assert_missing(exc)

def test_modify(sample) -> Explorer:
    service.create(sample)

    original_name: str = sample.name
    sample.country = "US"

    resp = service.modify(original_name, sample)
    assert resp.country == "US"

def test_modify_missing():
    pa: Explorer = Explorer(name="Pa Tuohy", description="The old sod", country="IE")
    with pytest.raises(Missing) as exc:
        _ = service.modify(pa.name, pa)
    assert_missing(exc)

def test_delete(sample):
    service.create(sample)
    resp = service.delete(sample.name)
    assert resp is True

def test_delete_missing():
    with pytest.raises(Missing) as exc:
        _ = service.delete("Pa Tuohy")
    assert_missing(exc)
