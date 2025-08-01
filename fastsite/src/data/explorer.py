from .init import curs, conn, IntegrityError
from errors import Missing, Duplicate
from model.explorer import Explorer

curs.execute("""CREATE TABLE IF NOT EXISTS explorer(
                name text primary key,
                country text,
                description text)""")

def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])

def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump() if explorer else None

def get_one(name: str) -> Explorer:
    qry: str = "SELECT * FROM explorer WHERE name=:name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found.")

def get_all() -> list[Explorer]:
    qry: str = "SELECT * FROM explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def create(explorer: Explorer) -> Explorer:
    qry: str = """INSERT INTO explorer (name, country, description) 
                  VALUES (:name, :country, :description)"""
    
    params = model_to_dict(explorer)
    try:
        _ = curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"Explorer {explorer.name} already exists.")
    
    return get_one(explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer): 
        return None

    qry: str = """UPDATE explorer
                  SET country=:country,
                      name=:name,
                      description=:description,
                  WHERE name=:name_orig"""
    
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    conn.commit()
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found.")

def delete(name: str) -> bool:
    if not name:
        return False
    
    qry: str = "DELETE FROM explorer WHERE name=:name"
    params: dict[str, str] = {"name": name}
    res = curs.execute(qry, params)
    conn.commit()
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found.")
    return bool(res)
