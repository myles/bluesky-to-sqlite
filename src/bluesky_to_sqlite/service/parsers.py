import datetime
from typing import TypedDict, Union

from atproto_client.models.app.bsky.actor.defs import (
    ProfileView,
    ProfileViewBasic,
    ProfileViewDetailed,
)
from atproto_client.models.app.bsky.feed.defs import PostView
from atproto_client.models.string_formats import DateTime


def parse_datetime(dt: Union[DateTime, None]) -> Union[datetime.datetime, None]:
    """
    Parses a DateTime object into a string that can be easily stored in a
    SQLite database.
    """
    if dt is None:
        return None
    return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")


class ParsedPost(TypedDict, total=False):
    uri: str
    cid: str
    author_did: str
    record_text: str
    record_created_at: Union[datetime.datetime, None]
    index_at: Union[datetime.datetime, None]


def parse_post(post: PostView) -> ParsedPost:
    """
    Parses a Post object into a dictionary that can be easily stored in a
    SQLite database.
    """
    record_text: str = post.record.text  # type: ignore
    record_created_at: Union[datetime.datetime, None] = parse_datetime(
        post.record.created_at  # type: ignore
    )
    return {
        "uri": post.uri,
        "cid": post.cid,
        "author_did": post.author.did,
        "record_text": record_text,
        "record_created_at": record_created_at,
        "index_at": parse_datetime(post.indexed_at),
    }


class ParsedProfile(TypedDict, total=False):
    did: str
    handle: str
    display_name: Union[str, None]
    description: Union[str, None]
    avatar: Union[str, None]
    pronouns: Union[str, None]
    created_at: Union[datetime.datetime, None]


def parse_profile(
    profile: Union[ProfileView, ProfileViewBasic, ProfileViewDetailed],
) -> ParsedProfile:
    """
    Parses a ProfileView object into a dictionary that can be easily stored in
    a SQLite database.
    """
    data: ParsedProfile = {
        "did": profile.did,
        "handle": profile.handle,
        "display_name": profile.display_name,
        "avatar": profile.avatar,
        "pronouns": profile.pronouns,
        "created_at": parse_datetime(profile.created_at),
    }

    if isinstance(profile, ProfileView) or isinstance(
        profile, ProfileViewDetailed
    ):
        data["description"] = profile.description

    return data
