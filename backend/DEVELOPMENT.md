# Development

Zeno's backend is a Python FastAPI server.

## Development Setup

Please read the [overall development setup](../DEVELOPMENT.md) before reading this.
Then follow the steps outlined here to run the backend locally.

The backend works with a postgres database.
To install postgres on macOS, use Homebrew: `brew install postgresql`.
Then, start the postgres service using `brew services start postgresql`.

To set up the server:

1. Enter a psql env `psql postgres`.
2. Add a new user `CREATE ROLE [username] WITH LOGIN PASSWORD '[password]';`.
3. Give the user rights to create a database `ALTER ROLE [username] CREATEDB;`.
4. Exit psql `\q` and re-enter it from that user `psql postgres -U [username]`.
5. Create a database `CREATE DATABASE zeno;`.
6. Grant your user privileges `GRANT ALL PRIVILEGES ON DATABASE zeno TO [username];`.
7. Bootstrap the initial tables by pasting the commands in [create_tables.sql](./create_tables.sql) into the PSQL terminal.

To inspect your data, you can install the [Postico GUI](https://eggerapps.at/postico2/) with brew `brew install --cask postico`.
The default host is `localhost` and port is `5432`.

Once this backend database is set up, the backend needs information on how to connect to it.
Therefore, add a `database.ini` in [./zeno_backend/database](./zeno_backend/database/) as follows:

```
[postgresql]
host=[whereever your DB is running, e.g. localhost:5432]
dbname=[the name of your DB]
user=[usename for DB login]
password=[password for DB login]
```

For the backend to be able to verify user status, the `ZENO_USER_POOL_AUTH_REGION`, `ZENO_USER_POOL_ID`, and `ZENO_USER_POOL_CLIENT_ID` environment variables are needed.
To simplify the dev setup, the zeno backend will try to read these from `../frontend/.env`.

For a debug setup, you can run `uvicorn zeno_backend.server:get_server --reload` from within the poetry shell.

### Static Analysis Tools

Ruff (linting), black (formatting), mypy (typechecking)

### Testing

pytest

### Guidelines:

- **Use Type Annotation:** Extensive type annotation is a key way to catch bugs in Python programs.
- **Prefer Data Structures over Dicts:** Dicts are flexible but don’t allow for type checking using static analysis. Instead, prefer using pydantic classes, which allows you to easily specify data structures.
- **Documentation:** All code should be documented (we will use the Google docstring standard). This will be enforced by linting.

## Deployment

To deploy the backend, you can either use the same setup as outlined for local development, or set environment variables instead of creating a `database.ini`.
You will have to set the following variables: `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

Additionally, you can configure the host and port for the backend using `BACKEND_HOST` and `BACKEND_PORT`, if not set, these default to `0.0.0.0` and `80`, respectively.
The backend can be started with poetry, from within the backend folder, run: `poetry run backend`.

To make sure that your frontend can access content from this backend even if running on another origin, use the `CORS_ORIGIN` environment variable to set CORS headers when requests come from the specified origin.
