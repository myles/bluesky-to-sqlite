from pathlib import Path

import click

from .core import save_followers, save_follows, save_like_posts
from .service.auth_file import create_auth_file, get_auth_file
from .service.client import get_client, verify_auth
from .service.db import open_database

cli_argument_db_path = click.argument(
    "db_file_path",
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        path_type=Path,
    ),
    required=True,
)

cli_option_auth_path = click.option(
    "-a",
    "--auth",
    "auth_file_path",
    type=click.Path(
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        path_type=Path,
    ),
    default="auth.json",
    help="Path to a JSON file containing your Bluesky authentication credentials.",
)


@click.group()
@click.version_option()
def cli():
    """
    Save data from your Bluesky to a SQLite database.
    """
    ...


@cli.command("auth")
@cli_option_auth_path
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite the authentication file if it already exists.",
)
def cli_auth(auth_file_path: Path, overwrite: bool = False):
    """Save your Bluesky authentication credentials to a JSON file."""
    if auth_file_path.exists() and overwrite is False:
        click.echo(f"Authentication file {auth_file_path} already exists.")
        overwrite = click.confirm("Do you want to overwrite it?")
        if not overwrite:
            click.echo("Aborting authentication setup.")
            return

    click.echo("Please enter your Bluesky authentication credentials.")

    pds_url = click.prompt(
        "PDS URL (e.g. https://bsky.social)", default="https://bsky.social"
    )

    username = click.prompt("Username (email or handle)")

    click.echo(
        "To generate an app password, go to https://bsky.app/settings/app-passwords and create a new app password. Use that password here."
    )
    password = click.prompt(
        "App password (https://bsky.app/settings/app-passwords)",
        hide_input=True,
    )

    # Before saving the credentials, we are going to try an authenticate with
    # the PDS.
    click.echo("Authenticating with Bluesky...")
    try:
        client = get_client(
            username=username, password=password, pds_url=pds_url
        )
        verify_auth(client)
        click.echo("Authentication successful!")
    except Exception as e:
        click.echo(f"Authentication failed: {e}")
        return

    create_auth_file(
        auth_file_path,
        pds_url=pds_url,
        username=username,
        password=password,
        overwrite=True,
    )
    click.echo(f"Authentication credentials saved to {auth_file_path}")


@cli.command("verify-auth")
@cli_option_auth_path
def cli_verify_auth(auth_file_path: Path):
    """
    Verify the authentication to the Mastodon server.
    """
    auth = get_auth_file(auth_file_path)
    client = get_client(**auth)

    try:
        verify_auth(client)
        click.echo("Successfully authenticated with the PDS.")
    except Exception as e:
        click.echo(f"Failed to authenticated with the PDS: {e}", err=True)


@cli.command("followers")
@cli_argument_db_path
@cli_option_auth_path
def cli_followers(db_file_path: Path, auth_file_path: Path):
    """
    Get the followers of the authenticated user.
    """
    db = open_database(db_file_path)

    auth = get_auth_file(auth_file_path)
    client = get_client(**auth)

    return save_followers(db, client)


@cli.command("follows")
@cli_argument_db_path
@cli_option_auth_path
def cli_follows(db_file_path: Path, auth_file_path: Path):
    """
    Get the follows of the authenticated user.
    """
    db = open_database(db_file_path)

    auth = get_auth_file(auth_file_path)
    client = get_client(**auth)

    return save_follows(db, client)


@cli.command("likes")
@cli_argument_db_path
@cli_option_auth_path
def cli_likes(db_file_path: Path, auth_file_path: Path):
    """
    Get the likes of the authenticated user.
    """
    db = open_database(db_file_path)

    auth = get_auth_file(auth_file_path)
    client = get_client(**auth)

    return save_like_posts(db, client)
