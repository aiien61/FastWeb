import os
import pytest
os.environ["CRYPTID_UNIT_TEST"] = "true"

from model.user import User
from src.service import user as service
from src.data.init import get_db, conn
from errors import Missing, Duplicate

@pytest.fixture
def sample() -> User:
    return User(name="faxfancy", hash="fancyhash")

@pytest.fixture(autouse=True)
def db_reset_and_teardown():
    get_db(reset=True)
    yield
    conn.execute("DELETE FROM user")
    conn.execute("DELETE FROM xuser")
    conn.commit()

def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.msg

def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.msg

def test_create(sample):
    resp = service.create(sample)
    assert resp == sample

def test_create_duplicate(sample):
    service.create(sample)
    with pytest.raises(Duplicate) as exc:
        _ = service.create(sample)
    assert_duplicate(exc)

def test_get_all():
    """
    Tests that get_all correctly retrieves all users from the database via the service and data layers.
    """
    # Arrange: Create some data directly in the database for the test.
    user1: User = User(name="user1", hash="pass1")
    user2: User = User(name="user2", hash="pass2")

    # Use the service's create function to set up the state.
    service.create(user1)
    service.create(user2)

    # Act
    result = service.get_all()

    # Assert: Check that the function returned the created data.
    # The order might not be guaranteed, so it's safer to check the contents and the length. 
    assert len(result) == 2

    # Convert results to a dictionary for easier lookup and assertion
    result_dict: dict[str, User] = {user.name: user for user in result}
    assert "user1" in result_dict
    assert "user2" in result_dict

    # Also check that the password was hashed correctly during creation
    assert service.verify_password("pass1", result_dict["user1"].hash)

def test_get_one_by_name(sample):
    service.create(sample)
    resp = service.get_one_by_name(sample.name)
    assert resp == sample

def test_get_one_missing(sample):
    with pytest.raises(Missing) as exc:
        _ = service.get_one_by_name("frogfancy")
    assert_missing(exc)

def test_modify(sample):
    service.create(sample)

    original_name: str = sample.name
    sample.hash = "faxyhash"

    resp = service.modify(original_name, sample)
    assert resp.hash == "faxyhash"

def test_modify_missing():
    frog = User(name="frogfancy", hash="fancyhash")
    with pytest.raises(Missing) as exc:
        _ = service.modify(frog.name, frog)
    assert_missing(exc)

def test_delete(sample):
    service.create(sample)
    resp = service.delete(sample.name)
    with pytest.raises(Missing) as exc:
        _ = service.get_one_by_name(sample.name)
    
    archived_user = service.get_one_by_name(sample.name, "xuser")
    assert archived_user.name == sample.name

def test_delete_missing():
    with pytest.raises(Missing) as exc:
        _ = service.delete("frogfancy")
    assert_missing(exc)

# ---

def test_auth_user_success(mocker):
    """
    Test successful user authentication by mocking the data layer.
    Verifies that the service layer correctly compares a plaintext password with a hashed password
    returned from the data layer.
    """
    # Setup: define the test data and the expected return from the mock
    test_name: str = "test_user"
    test_password: str = "plaintext_password"
    
    # Arrange
    hashed_password: str = service.get_hash(test_password)
    user_from_db: User = User(name=test_name, hash=hashed_password)

    # NOTE: Mock the data layer dependency 
    # Golden Rule of Patching: Patch 'data.get_one_by_name' in the namespace where it is USED 
    # ('service.user'), not where it is defined ('data.user').
    mock_get_one = mocker.patch("service.user.data.get_one_by_name")

    # NOTE: Configure the mock to return a specific value.
    # CONFIGURE MOCK: tell the mock what to return when called
    mock_get_one.return_value = user_from_db

    # EXECUTE: Call the tested function
    authenticated_user = service.auth_user(test_name, test_password)

    # ASSERT: Check the results
    # NOTE: Assert that the mock was called correctly. This tests the BEHAVIOUR of the function, 
    # not just its output.
    mock_get_one.assert_called_once_with(test_name)
    assert authenticated_user is not None
    assert authenticated_user.name == test_name

def test_auth_user_when_user_not_found(mocker):
    """
    Test authentication failure when the user does not exists.
    Verifies that the service layer handles the Missing exception from the data layer.
    """
    # Setup
    test_name: str = "non-existent-user"
    
    # Arrange
    mock_get_one = mocker.patch('service.user.data.get_one_by_name')
    # Configure the mock to simulate the data layer not finding the user and raise a missing error.
    mock_get_one.side_effect = Missing(msg=f"User {test_name} not found.")

    # Act
    result = service.auth_user(test_name, "any_password")
    
    # Assert
    assert result is None
    # Also verify that the data layer was called
    mock_get_one.assert_called_once_with(test_name)

def test_auth_user_when_wrong_password(mocker):
    """Test authentication failure when the password is incorrect."""

    # Arrange
    correct_password: str = "password123"
    wrong_password: str = "wrong_password"
    hashed_password: str = service.get_hash(correct_password)
    user_from_db: User = User(name="test_user", hash=hashed_password)
    mock_get_one = mocker.patch("service.user.data.get_one_by_name")
    mock_get_one.return_value = user_from_db

    # Act
    result = service.auth_user("test_user", wrong_password)

    # Assert
    assert result is None
    mock_get_one.assert_called_once_with("test_user")

def test_create_hashes_password(mocker, sample):
    """
    CRITICAL: Tests that the create service function hashes the password 
    before passing the user object to the data layer.
    """
    # Arrange
    # Mock the two dependencies of the 'create' function
    mock_get_hash = mocker.patch("service.user.get_hash")
    mock_data_create = mocker.patch("service.user.data.create")

    # Configure the return values for the mocks
    hashed_password: str = "a_mocked_hashed_password"
    mock_get_hash.return_value = hashed_password

    # The data layer should return the user with the now-hashed password
    expected_user_to_return = sample.copy(update={"hash": hashed_password})
    mock_data_create.return_value = expected_user_to_return

    # Act
    result = service.create(sample)

    # Assert
    # Was the password hashing function called with original plaintext password?
    # inspect the arguments passed to the mocks.
    mock_get_hash.assert_called_once_with("plaintext_password")

    # Was the data layer's create function called with the HASHED password?
    call_args, _ = mock_data_create.call_args
    user_object_passed_to_data = call_args[0]
    assert user_object_passed_to_data.hash == hashed_password

    # Did the function return the final user object correctly?
    assert result.hash == hashed_password

