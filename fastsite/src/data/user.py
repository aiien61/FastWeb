from model.user import User
from .init import conn, curs, get_db, IntegrityError
from errors import Missing, Duplicate

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

def model_to_dict(user: User) -> dict[str, str]:
    return user.model_dump()

def get_one_by_name(name: str, table: str = "user") -> User:
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

def create(user: User, table: str = "user") -> User:
    """Add <user> to user or xuser table"""
    qry: str = f"""INSERT INTO {table} (name, hash) VALUES (:name, :hash)"""
    params: dict[str, str] = model_to_dict(user)
    try:
        curs.execute(qry, params)
        # CRITICAL: Always commit after a write operation (INSERT, UPDATE, DELETE).
        # Without this, the change is never saved to the database file.
        conn.commit()

        # FIX: Pass the 'table' parameter down to get_one. This was a bug 
        # found during testing of the delete/archive feature.
        return get_one_by_name(user.name, table=table)
    
    except IntegrityError:
        # IMPORTANT: Rollback the transaction if an error occurs to leave the DB in a clean state.
        conn.rollback()
        raise Duplicate(msg=f"{table}: user {user.name} already exists.")

def modify(name: str, user: User) -> User:
    # FIX: The WHERE clause must use the original name to find the record.
    # The new name is in the SET clause.
    qry: str = """UPDATE user SET name=:name, hash=:hash WHERE name=:name_orig"""
    params: dict[str, str] = {"name": user.name, "hash": user.hash, "name_orig": name}
    curs.execute(qry, params)

    # NOTE: Checking rowcount ensures an update actually happened.
    if curs.rowcount == 1:
        # CRITICAL: Must commit after a successful UPDATE.
        conn.commit()
        return get_one_by_name(user.name)
    else:
        conn.rollback()
        raise Missing(msg=f"User {name} not found.")

def delete(name: str) -> None:
    """Drop user with <name> from user table, add to xuser table to archive"""
    # NOTE: This is a core piece of business logic in the data layer: "deleting" is "archiving".
    user: User = get_one_by_name(name)
    qry: str = "DELETE FROM user WHERE name = :name"
    params: dict[str, str] = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        conn.rollback()
        raise Missing(msg=f"User {name} not found.")
    
    # CRITICAL: Must commit the DELETE before attempting the archive INSERT.
    conn.commit()
    create(user, table="xuser")
    return None
