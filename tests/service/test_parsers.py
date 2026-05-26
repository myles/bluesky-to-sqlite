from bluesky_to_sqlite.service.parsers import parse_datetime, parse_profile
import datetime
from atproto_client.models.app.bsky.actor.defs import ProfileView


def test_parse_datetime():
    result = parse_datetime("2024-06-01T12:34:56.0Z")
    assert result == datetime.datetime(2024, 6, 1, 12, 34, 56)


def test_parse_datetime__none():
    result = parse_datetime(None)
    assert result is None


def test_parse_profile():
    profile = ProfileView(
        did="did:example:123",
        handle="user123",
        display_name="User 123",
        description="This is a test user.",
        avatar="https://example.com/avatar.jpg",
        pronouns="they/them",
        created_at="2024-06-01T12:34:56.0Z",
    )

    result = parse_profile(profile)
    assert result == {
        "did": "did:example:123",
        "handle": "user123",
        "display_name": "User 123",
        "description": "This is a test user.",
        "avatar": "https://example.com/avatar.jpg",
        "pronouns": "they/them",
        "created_at": datetime.datetime(2024, 6, 1, 12, 34, 56),
    }
