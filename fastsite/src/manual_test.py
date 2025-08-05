import os
import sys

# --- Setup the environment ---
# Tells the app to use an in-memory SOLite database for this session, protecting the real db file
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"

# Add the 'src' directory to Python's path to allow imports like 'from data import user'
sys.path.insert(0, "./src")

# --- Import the modules AFTER setting the environment ---
from model.user import User
from data import user as data_user
from data.init import conn
from errors import Missing, Duplicate


def main():
    """Run a sequence of manual tests."""
    print("--- Starting Manual Test ---")

    # 1. Test Create
    print("\n1. Testing CREATE...")
    try:
        sample_user = User(name="refield", hash="abc")
        created_user = data_user.create(sample_user)
        print(f"    SUCCESS: Created user -> {created_user}")
        assert created_user.name == "refield"
    except Exception as e:
        print(f"    FAILURE: {e}")
    
    # 2. Test Get One (Success)
    print("\n2. Testing GET ONE (Success)...")
    try:
        fetched_user = data_user.get_one("refield")
        print(f"    SUCCESS: Fetched user -> {fetched_user}")
        assert fetched_user.name == "refield"
    except Exception as e:
        print(f"    FAILURE: {e}")

    # 3. Test Get All
    print("\n3. Testing GET ALL...")
    try:
        all_users = data_user.get_all()
        print(f"    SUCCESS: All user -> {all_users}")
    except Exception as e:
        print(f"    FAILURE: {e}")

    # 4. Test Create (Duplicate)
    print("\n4. Testing CREATE (Duplicate)...")
    try:
        duplicate_user = User(name="refield", hash="xyz")
        data_user.create(duplicate_user)
        print(f"    FAILURE: Should have raised a Duplicate error!")
    except Duplicate as e:
        print(f"    SUCCESS: Correctly caught expected error -> {e}")

    # 5. Test Modify
    print("\n5. Testing MODIFY...")
    try:
        modified_user_data = User(name="refield", hash="new_password_123")
        modified_user = data_user.modify("refield", modified_user_data)
        print(f"    SUCCESS: Modified user -> {modified_user}")
        assert modified_user.hash == "new_password_123"
    except Exception as e:
        print(f"    FAILURE: {e}")

    # 6. Test Delete
    print("\n6. Testing DELETE...")
    try:
        # The delete function in your code is type-hinted to return None
        data_user.delete("refield")
        print("    SUCCESS: Delete function executed.")

        # Verify the side-effects of the deletion
        print("    Verifying deletion...")
        try:
            data_user.get_one("refield")  # should fail
            print("    FAILURE: User was not deleted from 'user' table!")
        except Missing:
            print("    SUCCESS: User is correctly missing from 'user' table.")
        
        print("    Verifying archival...")
        archived_user = data_user.get_one("refield", table="xuser")
        print(f"    SUCCESS: User was found in 'xuser' archive -> {archived_user}")
    
    except Exception as e:
        print(f"    FAILURE during delete process: {e}")

    
    print("\n--- Manual Test Complete ---")


if __name__ == "__main__":
    main()
