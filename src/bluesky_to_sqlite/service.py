import json
from pathlib import Path
from typing import Optional

from atproto import Client


def get_auth_file(auth_file_path: Path) -> dict:
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
    auth_data = {"pds_url": pds_url, "username": username, "password": password}
    with auth_file_path.open("w") as auth_file_obj:
        json.dump(auth_data, auth_file_obj, indent=2)


def get_client(
    username: str, password: str, pds_url: Optional[str] = None
) -> Client:
    client = Client(base_url=pds_url)
    client.login(login=username, password=password)
    return client


def verify_auth(client: Client):
    client.get_current_time()
    return True
