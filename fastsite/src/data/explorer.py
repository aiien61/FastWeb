from .init import curs, conn, IntegrityError
from errors import Missing, Duplicate
from model.explorer import Explorer

curs.execute("""CREATE TABLE IF NOT EXISTS explorer(
                name text primary key,
                country text,
                description text)""")

def row_to_model(row: tuple[str]) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])

def model_to_dict(explorer: Explorer) -> dict[str, str]:
    return explorer.model_dump() if explorer else None

def get_one_by_name(name: str) -> Explorer:
    qry: str = "SELECT * FROM explorer WHERE name=:name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    row: tuple[str] = curs.fetchone()
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
    
    params: dict[str, str] = model_to_dict(explorer)
    try:
        _ = curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"Explorer {explorer.name} already exists.")
    
    return get_one_by_name(explorer.name)

# MUST accept both arguments
# The 'name' is the original name from the URL, 'explorer.name' could be the new name
def modify(name: str, explorer: Explorer) -> Explorer:
    # if not (name and explorer): 
    #     return None

    qry: str = """UPDATE explorer
                  SET country=:country,
                      name=:name,
                      description=:description
                  WHERE name=:name_orig"""
    
    params: dict[str, str] = model_to_dict(explorer)
    params["name_orig"] = name
    _ = curs.execute(qry, params)
    if curs.rowcount == 1:
        conn.commit()
        return get_one_by_name(explorer.name)
    else:
        conn.rollback()
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
