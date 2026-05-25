from atproto import Client
from sqlite_utils import Database

from bluesky_to_sqlite.service.client import get_followers, get_follows
from bluesky_to_sqlite.service.db import (
    build_database,
    save_following,
    save_profiles,
)
from bluesky_to_sqlite.service.parsers import parse_profile


def save_followers(db: Database, client: Client):
    """
    Save the followers to the database.
    """
    if not client.me:
        raise ValueError(
            "Client is not authenticated. Please authenticate before saving followers."
        )

    build_database(db)

    parsed_me = parse_profile(client.me)

    profiles_to_save = [parsed_me]
    for profile in get_followers(client.me.did, client):
        parsed_profile = parse_profile(profile)
        profiles_to_save.append(parsed_profile)

    followings_to_save = []
    for profile in profiles_to_save:
        followings_to_save.append((profile["did"], parsed_me["did"]))

    save_profiles(profiles_to_save, db)
    save_following(followings_to_save, db)


def save_follows(db: Database, client: Client):
    """
    Save the follows to the database.
    """
    if not client.me:
        raise ValueError(
            "Client is not authenticated. Please authenticate before saving followers."
        )

    build_database(db)

    parsed_me = parse_profile(client.me)

    profiles_to_save = [parsed_me]
    for profile in get_follows(client.me.did, client):
        parsed_profile = parse_profile(profile)
        profiles_to_save.append(parsed_profile)

    followings_to_save = []
    for profile in profiles_to_save:
        followings_to_save.append((parsed_me["did"], profile["did"]))

    save_profiles(profiles_to_save, db)
    save_following(followings_to_save, db)
