from atproto import Client
from sqlite_utils import Database

from .service.client import get_followers, get_follows, get_likes, get_posts
from .service.db import (
    build_database,
    save_following,
    save_likes,
    save_posts,
    save_profiles,
)
from .service.parsers import parse_post, parse_profile, parse_like


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

    post_uris = []
    likes_to_save = []
    for like in likes:
        post_uris.append(like.value.subject.uri)  # type: ignore
        likes_to_save.append(parse_like(actor_did=client.me.did, like=like))

    posts = get_posts(post_uris, client)

    posts_to_save = []
    profiles_to_save = []
    for post in posts:
        parsed_post = parse_post(post)
        posts_to_save.append(parsed_post)

        parsed_author = parse_profile(post.author)
        profiles_to_save.append(parsed_author)

    save_profiles(profiles_to_save, db)
    save_posts(posts_to_save, db)
    save_likes(likes_to_save, db)
