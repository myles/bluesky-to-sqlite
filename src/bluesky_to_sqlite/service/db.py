from pathlib import Path
from typing import List

from sqlite_utils.db import Database, Table

from .parsers import ParsedLike, ParsedPost, ParsedProfile


def open_database(db_file_path: Path) -> Database:
    """Open the SQLite database."""
    return Database(db_file_path)


def get_table(table_name: str, db: Database) -> Table:
    """
    Returns a Table from a given db Database object.
    """
    return Table(db=db, name=table_name)


def build_database(db: Database):
    """Build the database schema if it doesn't already exist."""

    # Create the actors table if it doesn't already exist.
    profiles_table = get_table("actors", db)
    if profiles_table.exists() is False:
        profiles_table.create(
            columns={
                "did": str,
                "handle": str,
                "display_name": str,
                "description": str,
                "avatar": str,
                "pronouns": str,
                "created_at": str,
            },
            pk="did",
        )

    # Create the following table if it doesn't already exist.
    following_table: Table = get_table("following", db)
    if following_table.exists() is False:
        following_table.create(
            columns={"follower_did": str, "followed_did": str},
            pk=["follower_did", "followed_did"],
            foreign_keys=(
                ("follower_did", "actors", "did"),
                ("followed_did", "actors", "did"),
            ),
        )

    following_indexes = {tuple(i.columns) for i in following_table.indexes}
    if ("follower_did",) not in following_indexes:
        following_table.create_index(["follower_did"])
    if ("followed_did",) not in following_indexes:
        following_table.create_index(["followed_did"])

    # Create the posts table if it doesn't already exist.
    posts_table: Table = get_table("posts", db)
    if posts_table.exists() is False:
        posts_table.create(
            columns={
                "uri": str,
                "cid": str,
                "author_did": str,
                "record_text": str,
                "record_created_at": str,
                "indexed_at": str,
            },
            pk="cid",
            foreign_keys=(("author_did", "profiles", "did"),),
        )

    posts_indexes = {tuple(i.columns) for i in posts_table.indexes}
    if ("author_did",) not in posts_indexes:
        posts_table.create_index(["author_did"])

    likes_table: Table = get_table("likes", db)
    if likes_table.exists() is False:
        likes_table.create(
            columns={
                "liker_did": str,
                "post_cid": str,
                "liked_at": str,
            },
            pk=["liker_did", "post_cid"],
            foreign_keys=(
                ("liker_did", "profiles", "did"),
                ("post_cid", "posts", "cid"),
            ),
        )

    likes_indexes = {tuple(i.columns) for i in likes_table.indexes}
    if ("liker_did",) not in likes_indexes:
        likes_table.create_index(["liker_did"])
    if ("post_cid",) not in likes_indexes:
        likes_table.create_index(["post_cid"])


def save_posts(posts: List[ParsedPost], db: Database):
    """Save a list of posts to the database."""
    posts_table = get_table("posts", db)
    posts_table.upsert_all(posts, pk="cid")


def save_profiles(profiles: List[ParsedProfile], db: Database):
    """Save a list of profiles to the database."""
    profiles_table = get_table("profiles", db)
    profiles_table.upsert_all(profiles, pk="did")


def save_following(following: List[tuple[str, str]], db: Database):
    """Save a list of following relationships to the database."""
    following_table = get_table("following", db)
    following_table.upsert_all(
        [{"follower_did": f[0], "followed_did": f[1]} for f in following],
        pk=["follower_did", "followed_did"],
    )


def save_likes(likes: List[ParsedLike], db: Database):
    """Save a list of likes to the database."""
    likes_table = get_table("likes", db)
    likes_table.upsert_all(likes, pk=["liker_did", "post_cid"])
