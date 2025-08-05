from model.user import User
from .init import conn, curs, get_db, IntegrityError
from errors import Missing, Duplicate
from icecream import ic

curs.execute("""
             CREATE TABLE IF NOT EXISTS
             user(name text primary key, 
                  hash text)
             """)

curs.execute("""
             CREATE TABLE IF NOT EXISTS
             xuser(name text primary key, 
                   hash text)
             """)

def row_to_model(row: tuple[str]) -> User:
    name, hash = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    return user.model_dump()

def get_one(name: str, table: str = "user") -> User:
    qry: str = f"SELECT * FROM {table} WHERE name=:name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    row: tuple[str, str] = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found.")
    
def get_all() -> list[User]:
    qry: str = "SELECT * FROM user"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def create(user: User, table: str = "user"):
    """Add <user> to user or xuser table"""
    qry: str = f"""INSERT INTO {table} (name, hash) VALUES (:name, :hash)"""
    params: dict[str, str] = model_to_dict(user)
    try:
        curs.execute(qry, params)
        conn.commit()
        return get_one(user.name, table=table)
    except IntegrityError:
        conn.rollback()
        raise Duplicate(msg=f"{table}: user {user.name} already exists.")

def modify(name: str, user: User) -> User:
    qry: str = """UPDATE user SET name=:name, hash=:hash WHERE name=:name_orig"""
    params = {"name": user.name, "hash": user.hash, "name_orig": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        conn.commit()
        return get_one(user.name)
    else:
        conn.rollback()
        raise Missing(msg=f"User {name} not found.")

def delete(name: str) -> None:
    """Drop user with <name> from user table, add to xuser table to archive"""
    user = get_one(name)
    qry: str = "DELETE FROM user WHERE name = :name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        conn.rollback()
        raise Missing(msg=f"User {name} not found.")
    conn.commit()
    create(user, table="xuser")
    return None
