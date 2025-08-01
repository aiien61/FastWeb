from model.explorer import Explorer
from service import explorer as code
from fake.explorer import _explorers

sample = Explorer(name="Claude Hande",
                  country="FR",
                  description="Scarce during full moons")

def test_get_all():
    resp = code.get_all()
    print(resp)
    assert resp == _explorers

def test_get_one():
    resp = code.get_one(sample.name)
    assert resp == sample

# def test_create():


# def create(explorer: Explorer) -> Explorer:
#     return data.create(explorer)

# def replace(id: int, explorer: Explorer) -> Explorer:
#     return data.replace(id, explorer)

# def modify(id: int, explorer: Explorer) -> Explorer:
#     return data.modify(id, explorer)

# def delete(id: int, explorer: Explorer)