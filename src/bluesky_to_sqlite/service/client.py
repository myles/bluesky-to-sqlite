from typing import Generator, Optional, Union

from atproto import Client
from atproto_client.models.app.bsky.actor.defs import (
    ProfileView,
    ProfileViewDetailed,
)
from atproto_client.models.app.bsky.feed.defs import FeedViewPost


def get_client(
    username: str, password: str, pds_url: Optional[str] = None
) -> Client:
    """
    Returns an authenticated AtProto Client instance.
    """
    client = Client(base_url=pds_url)
    client.login(login=username, password=password)
    return client


def verify_auth(client: Client):
    """
    Small utility function to verify that the provided client is authenticated.
    """
    client.get_current_time()
    return True


def get_profile(actor: str, client: Client) -> ProfileViewDetailed:
    """
    Returns the profile of the given actor.
    """
    return client.get_profile(actor)


def get_followers(
    actor: str, client: Client
) -> Generator[ProfileView, None, None]:
    """
    Returns a list of followers for the authenticated user.
    """
    cursor: Union[str, None] = ""
    while cursor is not None:
        result = client.get_followers(actor, limit=50, cursor=cursor)
        cursor = result.cursor
        for follower in result.followers:
            yield follower


def get_follows(
    actor: str, client: Client
) -> Generator[ProfileView, None, None]:
    """
    Returns a list of followers for the authenticated user.
    """
    cursor: Union[str, None] = ""
    while cursor is not None:
        result = client.get_follows(actor, limit=50, cursor=cursor)
        cursor = result.cursor
        for follower in result.follows:
            yield follower


def get_likes(
    actor: str, client: Client
) -> Generator[FeedViewPost, None, None]:
    """
    Returns a list of likes for the authenticated user.
    """
    cursor: Union[str, None] = ""
    while cursor is not None:
        result = client.app.bsky.feed.get_actor_likes(
            dict(actor=actor, limit=50, cursor=cursor)
        )
        cursor = result.cursor
        for like in result.feed:
            yield like
