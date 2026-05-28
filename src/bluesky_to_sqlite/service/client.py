from atproto_client.namespaces.async_ns import AppBskyFeedLikeRecord
import logging
from typing import Generator, Optional, Union, List

from atproto import Client
from atproto_client.models.app.bsky.actor.defs import (
    ProfileView,
    ProfileViewDetailed,
)
from atproto_client.models.app.bsky.feed.defs import FeedViewPost, PostView
from atproto_client.models.com.atproto.repo.list_records import Record as ListRecordsRecord


logger = logging.getLogger(__name__)


def get_client(
    username: str, password: str, pds_url: Optional[str] = None
) -> Client:
    """
    Returns an authenticated AtProto Client instance.
    """
    client = Client(base_url=pds_url)
    client.login(login=username, password=password)

    logger.debug("Authenticated client for user: %s", username)

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
    logger.debug("Fetching profile for actor: %s", actor)
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

        logger.debug("Fetched %d followers for actor: %s", len(result.followers), actor)


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

        logger.debug("Fetched %d follows for actor: %s", len(result.follows), actor)


def get_likes(
    actor_id: str, client: Client
) -> Generator[ListRecordsRecord, None, None]:
    """
    Returns a list of likes for the authenticated user.
    """
    cursor: Union[str, None] = ""
    while cursor is not None:
        result = client.com.atproto.repo.list_records(
            dict(
                repo=actor_id,
                collection="app.bsky.feed.like",
                limit=50,
                cursor=cursor,
            )
        )

        if len(result.records) == 0:
            cursor = None
        else:
            cursor = result.cursor

        for record in result.records:
            yield record

        logger.debug("Fetched %d likes for actor: %s", len(result.records), actor_id)


def get_posts(uris: List[str], client: Client) -> Generator[PostView, None, None]:
    """
    Returns a list of posts for the given URIs.
    """
    # The app.bsky.feed.getPosts endpoint can only handle 25 URIs at a time, so we need to batch the requests.
    uris_batch_size = 25
    uri_chunks = [uris[i:i + uris_batch_size] for i in range(0, len(uris), uris_batch_size)]

    for chunk in uri_chunks:
        result = client.app.bsky.feed.get_posts(dict(uris=chunk))
        for post in result.posts:
            yield post
