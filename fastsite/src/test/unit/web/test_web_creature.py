from fastapi import HTTPException
import pytest
import os
os.environ["CRYPTID_UNIT_TEST"] = "true"
from model.creature import Creature
from src.web import creature
from fake import creature as fake_creature

@pytest.fixture(autouse=True)
def reset_fake_creature_for_web():
    fake_creature._creatures = []
    yield

@pytest.fixture
def sample() -> Creature:
    return Creature(name="dragon", description="Wings! Fire! Aieee!", country="*")

# @pytest.fixture
# def fakes() -> list[Creature]:
#     return creature.get_all()

def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail

def test_create(sample):
    assert creature.create(sample) == sample

def test_create_duplicate(sample):
    creature.create(sample)
    with pytest.raises(HTTPException) as exc:
        _ = creature.create(sample)
    assert_duplicate(exc)

def test_get_one(sample):
    creature.create(sample)
    assert creature.get_one(sample.name) == sample

def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        _ = creature.get_one("bobcat")
        assert_missing(exc)

def test_modify(sample):
    creature.create(sample)
    sample.description = "Actually very friendly"
    assert creature.modify(sample.name, sample) == sample

def test_modify_missing(sample):
    with pytest.raises(HTTPException) as exc:
        _ = creature.modify(sample.name, sample)
    assert_missing(exc)

def test_delete(sample):
    creature.create(sample)
    assert creature.delete(sample.name) is None

def test_delete_missing(sample):
    with pytest.raises(HTTPException) as exc:
        _ = creature.delete(sample.name)
        assert_missing(exc)
