# bluesky-to-sqlite

Save data from your Bluesky account to a SQLite database.

Part of the [Dogsheep](https://dogsheep.github.io/) family of `*-to-sqlite` tools, built on [sqlite-utils](https://sqlite-utils.datasette.io/).

> [!WARNING]
> This tool is in early development and has a limited feature set. Use at your own risk. The database schema is subject to change without warning.

## Usage

### Install the package

Right now, this package isn't published to PyPI, so you'll need to install it directly from GitHub. You can do this with pip or pipx.

Install with pip:

```bash
pip install git+https://github.com/myles/bluesky-to-sqlite.git
```

or with [pipx](https://pipx.pypa.io/):

```bash
pipx install git+https://github.com/myles/bluesky-to-sqlite.git
```

### Authenticate with Bluesky

Before you can pull any data, you need to authenticate with your PDS (Personal Data Server). You'll provide your PDS URL, your username, and an [app password](https://bsky.app/settings/app-passwords) — not your account password.

Run:

```bash
$ bluesky-to-sqlite auth
Please enter your Bluesky authentication credentials.
PDS URL (e.g. https://bsky.social) [https://bsky.social]: https://pds.witchcraft.systems
Username (email or handle): myles.garden
To generate an app password, go to https://bsky.app/settings/app-passwords and create a new app password. Use that password here.
App password (https://bsky.app/settings/app-passwords):
Authenticating with Bluesky...
Authentication successful!
Authentication credentials saved to auth.json
```

This writes your credentials to `auth.json` in the current directory. If that file already exists, you'll be asked whether to overwrite it.

The data commands below read `auth.json` from the current directory, so run them from the same place — or see `--help` to point at a different path.

### Save data to SQLite

There are a few different commands for pulling data out of your Bluesky account. Each takes a path to the SQLite database to write to, which will be created if it doesn't already exist:

```bash
bluesky-to-sqlite <command> bluesky.db
```

#### Posts you liked

Save the posts you have liked:

```bash
bluesky-to-sqlite likes bluesky.db
```

#### Accounts you are following

Save the accounts you follow into a `following` table:

```bash
bluesky-to-sqlite follows bluesky.db
```

#### Accounts that are following you

Save the accounts that follow you into a `followers` table:

```bash
bluesky-to-sqlite followers bluesky.db
```
