from model.creature import Creature
from service import creature as code
from fake.creature import _creatures

sample = Creature(name="Yeti", 
                  aka="Abominable Snowman",
                  country="NPL",
                  area="Himalayas",
                  description="Hirsute Himalayan")

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample

def test_get_missing():
    resp = code.get_one("Boxturtle")
    assert resp is None

def test_get_all():
    resp = code.get_all()
    assert resp == _creatures

def test_modify():
    sample.description = "Snowman"
    code.modify(0, sample)
    resp = code.get(0)
    assert resp == sample

def test_delete_success():
    sample = Creature(name="Dragon",
                      description="A winged, fire-breathing creature",
                      country="*",
                      area="*",
                      aka="Charizard")
    resp = code.delete(1, sample)
    assert resp is True

def test_delete_failure():
    resp = code.delete(0, sample)
    assert resp is False
