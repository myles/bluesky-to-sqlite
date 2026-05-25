from pathlib import Path

import click

from . import service

cli_option_auth_file = click.option(
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


@cli.command()
@cli_option_auth_file
def auth(auth_file_path: Path):
    """Save your Bluesky authentication credentials to a JSON file."""
    if auth_file_path.exists():
        click.echo(f"Authentication file {auth_file_path} already exists.")
        if not click.confirm("Do you want to overwrite it?"):
            click.echo("Aborting authentication setup.")
            return

    click.echo("Please enter your Bluesky authentication credentials.")

    pds_url = click.prompt(
        "PDS URL (e.g. https://bsky.app)", default="https://bsky.app"
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
        client = service.get_client(
            username=username, password=password, pds_url=pds_url
        )
        service.verify_auth(client)
        click.echo("Authentication successful!")
    except Exception as e:
        click.echo(f"Authentication failed: {e}")
        return

    service.create_auth_file(
        auth_file_path, pds_url=pds_url, username=username, password=password
    )
    click.echo(f"Authentication credentials saved to {auth_file_path}")


@cli.command()
@cli_option_auth_file
def verify_auth(auth_file_path: Path):
    """
    Verify the authentication to the Mastodon server.
    """
    auth = service.get_auth_file(auth_file_path)
    client = service.get_client(**auth)

    try:
        service.verify_auth(client)
        click.echo("Successfully authenticated with the PDS.")
    except Exception as e:
        click.echo(f"Failed to authenticated with the PDS: {e}", err=True)
