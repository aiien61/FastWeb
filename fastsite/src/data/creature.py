from .init import conn, curs, IntegrityError
from model.creature import Creature
from errors import Missing, Duplicate

curs.execute("""CREATE TABLE IF NOT EXISTS creature(
             name text primary key,
             description text,
             country text,
             area text,
             aka text)""")

def row_to_model(row: tuple) -> Creature:
    name, description,country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)

def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()

def get_one(name: str) -> Creature:
    qry: str = "SELECT * FROM creature WHERE name = :name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()

    if not row:
        raise Missing(msg=f"Creature {name} not found.")

    return row_to_model(row)

def get_all(name: str) -> list[Creature]:
    qry = "SELECT * FROM creature"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]

def create(creature: Creature):
    qry = """INSERT INTO creature VALUES (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"Creature {creature.name} already exists.")
    
    return get_one(creature.name)

def modify(creature: Creature) -> Creature:
    qry = """UPDATE creature
             SET country=:country,
                 name=:name,
                 description=:description,
                 area=:area,
                 aka=:aka
             WHERE name=:name_orig"""
    
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = curs.execute(qry, params)
    return get_one(creature.name)

def replace(creature: Creature):
    return creature

def delete(name: str):
    qry = "DELETE FROM creature WHERE name = :name"
    params = {"name": name}
    res = curs.execute(qry, params)

    if res.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found.")
    
    conn.commit()
    return True
