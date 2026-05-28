import datetime

import pytest
from atproto_client.models.app.bsky.actor.defs import ProfileView, ProfileViewBasic
from atproto_client.models.app.bsky.feed.defs import PostView
from atproto_client.models.app.bsky.feed.like import Record as LikeRecord
from atproto_client.models.app.bsky.feed.post import Record as PostRecord
from atproto_client.models.com.atproto.repo.list_records import (
    Record as ListRecordsRecord,
)
from atproto_client.models.com.atproto.repo.strong_ref import Main as StrongRef

from bluesky_to_sqlite.service.parsers import (
    parse_datetime,
    parse_like,
    parse_post,
    parse_profile,
)


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


def test_parse_post():
    author = ProfileViewBasic(did="did:plc:author123", handle="author.bsky.social")
    record = PostRecord(text="Hello world", created_at="2024-06-01T12:34:56.0Z")
    post = PostView(
        uri="at://did:plc:author123/app.bsky.feed.post/abc123",
        cid="bafyreiabc123",
        author=author,
        record=record,
        indexed_at="2024-06-01T12:35:00.0Z",
    )

    result = parse_post(post)
    assert result == {
        "uri": "at://did:plc:author123/app.bsky.feed.post/abc123",
        "cid": "bafyreiabc123",
        "author_did": "did:plc:author123",
        "record_text": "Hello world",
        "record_created_at": datetime.datetime(
            2024, 6, 1, 12, 34, 56, tzinfo=datetime.timezone.utc
        ),
        "indexed_at": datetime.datetime(
            2024, 6, 1, 12, 35, 0, tzinfo=datetime.timezone.utc
        ),
    }


def test_parse_like():
    subject = StrongRef(
        cid="bafyreiabc123",
        uri="at://did:plc:author123/app.bsky.feed.post/abc123",
    )
    like_record = LikeRecord(created_at="2024-06-02T10:00:00.0Z", subject=subject)
    list_record = ListRecordsRecord(
        cid="bafyreilikeXYZ",
        uri="at://did:plc:liker456/app.bsky.feed.like/xyz789",
        value=like_record,
    )

    result = parse_like(actor_did="did:plc:liker456", like=list_record)
    assert result == {
        "liker_did": "did:plc:liker456",
        "post_cid": "bafyreiabc123",
        "liked_at": datetime.datetime(2024, 6, 2, 10, 0, 0, tzinfo=datetime.timezone.utc),
    }


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


def test_parse_profile__basic_omits_description():
    profile = ProfileViewBasic(
        did="did:example:456",
        handle="basic.bsky.social",
        display_name="Basic User",
        avatar="https://example.com/avatar2.jpg",
        created_at="2024-07-01T08:00:00.0Z",
    )

    result = parse_profile(profile)
    assert "description" not in result
    assert result == {
        "did": "did:example:456",
        "handle": "basic.bsky.social",
        "display_name": "Basic User",
        "avatar": "https://example.com/avatar2.jpg",
        "pronouns": None,
        "created_at": datetime.datetime(
            2024, 7, 1, 8, 0, 0, tzinfo=datetime.timezone.utc
        ),
    }
