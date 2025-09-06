from .init import conn, curs, IntegrityError
from model.creature import Creature
from errors import Missing, Duplicate

curs.execute("""CREATE TABLE IF NOT EXISTS creature(
             name text primary key,
             description text,
             country text,
             area text,
             aka text)""")

def row_to_model(row: tuple[str]) -> Creature:
    name, description,country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)

def model_to_dict(creature: Creature) -> dict[str, str]:
    return creature.model_dump()

def get_one_by_name(name: str) -> Creature:
    qry: str = "SELECT * FROM creature WHERE name = :name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    row: tuple[str] = curs.fetchone()

    if not row:
        raise Missing(msg=f"Creature {name} not found.")

    return row_to_model(row)

def get_all() -> list[Creature]:
    qry: str = "SELECT * FROM creature"
    curs.execute(qry)
    rows: list[tuple] = list(curs.fetchall())
    return [row_to_model(row) for row in rows]

def create(creature: Creature) -> Creature:
    qry: str = """INSERT INTO creature VALUES (:name, :description, :country, :area, :aka)"""
    params: dict[str, str] = model_to_dict(creature)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"Creature {creature.name} already exists.")
    
    return get_one_by_name(creature.name)

def modify(name:str, creature: Creature) -> Creature:
    qry = """UPDATE creature
             SET country=:country,
                 name=:name,
                 description=:description,
                 area=:area,
                 aka=:aka
             WHERE name=:name_orig"""
    
    params: dict[str, str] = model_to_dict(creature)
    params["name_orig"] = name
    curs.execute(qry, params)
    if curs.rowcount == 1:
        conn.commit()
        return get_one_by_name(creature.name)
    else:
        conn.rollback()
        raise Missing(msg=f"Creature {creature.name} not found to modify.")

def delete(name: str):
    qry = "DELETE FROM creature WHERE name = :name"
    params: dict[str, str] = {"name": name}
    res = curs.execute(qry, params)

    if res.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found.")
    
    conn.commit()
    return True
