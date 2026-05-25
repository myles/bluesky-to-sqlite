import json
from pathlib import Path
from typing import TypedDict


class AuthData(TypedDict):
    pds_url: str
    username: str
    password: str


def get_auth_file(auth_file_path: Path) -> AuthData:
    """
    Reads the authentication file and returns the authentication data as
    a dictionary.
    """
    if not auth_file_path.exists():
        raise FileNotFoundError(
            f"Authentication file {auth_file_path} does not exist."
        )
    with auth_file_path.open() as auth_file_obj:
        auth_data = auth_file_obj.read()
    return json.loads(auth_data)


def create_auth_file(
    auth_file_path: Path, *, pds_url: str, username: str, password: str
):
    """
    Creates an authentication file with the provided PDS URL, username,
    and password. The authentication data is stored in JSON format.
    """
    auth_data = {"pds_url": pds_url, "username": username, "password": password}
    with auth_file_path.open("w") as auth_file_obj:
        json.dump(auth_data, auth_file_obj, indent=2)
