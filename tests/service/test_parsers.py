import pytest
from bluesky_to_sqlite.service.parsers import parse_datetime, parse_profile
import datetime
from atproto_client.models.app.bsky.actor.defs import ProfileView


@pytest.mark.parametrize(
    "input_str, expected_dt",
    [
        (
            "2024-06-01T12:34:56.0Z",
            datetime.datetime(
                2024, 6, 1, 12, 34, 56, tzinfo=datetime.timezone.utc
            ),
        ),
        (
            "2025-09-12T13:56:14.748987+00:00",
            datetime.datetime(
                2025, 9, 12, 13, 56, 14, 748987, tzinfo=datetime.timezone.utc
            ),
        ),
        (None, None),
    ],
)
def test_parse_datetime(input_str: str, expected_dt: datetime.datetime):
    result = parse_datetime(input_str)
    assert result == expected_dt


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
        "created_at": datetime.datetime(
            2024, 6, 1, 12, 34, 56, tzinfo=datetime.timezone.utc
        ),
    }
