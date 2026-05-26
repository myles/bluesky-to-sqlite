from atproto import Client
from sqlite_utils import Database

from .service.client import get_followers, get_follows, get_likes
from .service.db import (
    build_database,
    save_following,
    save_profiles,
save_likes,
save_posts
)
from .service.parsers import parse_profile, parse_post,parse_datetime, parse_post, parse_profile


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


def save_like_posts(db: Database, client: Client):
    """
    Save the liked posts to the database.
    """
    if not client.me:
        raise ValueError(
            "Client is not authenticated. Please authenticate before saving followers."
        )

    build_database(db)

    likes = get_likes(client.me.did, client)

    likes_to_save = []
    posts_to_save = []
    profiles_to_save = []
    for like in likes:
        likes_to_save.append((like.post.cid, client.me.did, None))

        parsed_post = parse_post(like.post)
        posts_to_save.append(parsed_post)

        parsed_author = parse_profile(like.post.author)
        profiles_to_save.append(parsed_author)

    save_profiles(profiles_to_save, db)
    save_posts(posts_to_save, db)
    save_likes(likes_to_save, db)
