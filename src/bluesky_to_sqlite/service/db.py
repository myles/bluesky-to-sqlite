from pathlib import Path
from typing import List

from sqlite_utils.db import Database, Table

from .parsers import ParsedProfile


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


def save_profiles(profiles: List[ParsedProfile], db: Database):
    """Save a list of profiles to the database."""
    profiles_table = get_table("profiles", db)
    profiles_table.insert_all(profiles, pk="did", replace=True)


def save_following(following: List[tuple[str, str]], db: Database):
    """Save a list of following relationships to the database."""
    following_table = get_table("following", db)
    following_table.insert_all(
        [{"follower_did": f[0], "followed_did": f[1]} for f in following],
        pk=["follower_did", "followed_did"],
        replace=True,
    )
