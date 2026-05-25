import datetime
from typing import TypedDict, Union

from atproto_client.models.app.bsky.actor.defs import (
    ProfileView,
    ProfileViewDetailed,
)
from atproto_client.models.string_formats import DateTime


def parse_datetime(dt: Union[DateTime, None]) -> Union[datetime.datetime, None]:
    """
    Parses a DateTime object into a string that can be easily stored in a
    SQLite database.
    """
    if dt is None:
        return None
    return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")


class ParsedProfile(TypedDict):
    did: str
    handle: str
    display_name: Union[str, None]
    description: Union[str, None]
    avatar: Union[str, None]
    pronouns: Union[str, None]
    created_at: Union[datetime.datetime, None]


def parse_profile(
    profile: Union[ProfileView, ProfileViewDetailed],
) -> ParsedProfile:
    """
    Parses a ProfileView object into a dictionary that can be easily stored in
    a SQLite database.
    """
    return {
        "did": profile.did,
        "handle": profile.handle,
        "display_name": profile.display_name,
        "description": profile.description,
        "avatar": profile.avatar,
        "pronouns": profile.pronouns,
        "created_at": parse_datetime(profile.created_at),
    }
