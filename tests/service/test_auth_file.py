import pytest
import json
from bluesky_to_sqlite.service.auth_file import get_auth_file, create_auth_file


def test_get_auth_file(tmp_path):
    file_path = tmp_path / "auth.json"

    with file_path.open("w") as file_obj:
        json.dump(
            {
                "pds_url": "https://example.com",
                "username": "user",
                "password": "pass",
            },
            file_obj,
            indent=2,
        )

    auth = get_auth_file(file_path)
    assert auth == {
        "pds_url": "https://example.com",
        "username": "user",
        "password": "pass",
    }


def test_get_auth_file__not_found(tmp_path):
    with pytest.raises(FileNotFoundError) as exc_info:
        get_auth_file(tmp_path / "nonexistent.json")
    assert (
        str(exc_info.value)
        == f"Authentication file {tmp_path / 'nonexistent.json'} does not exist."
    )


def test_get_auth_file__missing_fields(tmp_path):
    file_path = tmp_path / "auth.json"

    with file_path.open("w") as file_obj:
        json.dump({"pds_url": "https://example.com"}, file_obj, indent=2)

    with pytest.raises(ValueError) as exc_info:
        get_auth_file(file_path)
    assert (
        str(exc_info.value)
        == f"Authentication file {file_path} is missing required fields."
    )


def test_create_auth_file(tmp_path):
    file_path = tmp_path / "auth.json"
    create_auth_file(
        file_path,
        pds_url="https://example.com",
        username="user",
        password="pass",
    )

    with file_path.open() as file_obj:
        auth_data = json.load(file_obj)

    assert auth_data == {
        "pds_url": "https://example.com",
        "username": "user",
        "password": "pass",
    }


def test_create_auth_file__overwrite(tmp_path):
    file_path = tmp_path / "auth.json"

    # Create an initial auth file
    create_auth_file(
        file_path,
        pds_url="https://example.com",
        username="user",
        password="pass",
    )

    # Overwrite the auth file with new data
    with pytest.raises(FileExistsError) as exc_info:
        create_auth_file(
            file_path,
            pds_url="https://newexample.com",
            username="newuser",
            password="newpass",
            overwrite=False,
        )
    assert (
        str(exc_info.value)
        == f"Authentication file {file_path} already exists."
    )

    create_auth_file(
        file_path,
        pds_url="https://newexample.com",
        username="newuser",
        password="newpass",
        overwrite=True,
    )

    with file_path.open() as file_obj:
        auth_data = json.load(file_obj)

    assert auth_data == {
        "pds_url": "https://newexample.com",
        "username": "newuser",
        "password": "newpass",
    }
