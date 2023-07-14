# Development

Zeno's backend is a Python FastAPI server.

## Development Setup

Please read the [overall development setup](../DEVELOPMENT.md) before reading this.

### Static Analysis Tools

Ruff (linting), black (formatting), mypy (typechecking)

### Testing

pytest

### Guidelines:

- **Use Type Annotation:** Extensive type annotation is a key way to catch bugs in Python programs.
- **Prefer Data Structures over Dicts:** Dicts are flexible but don’t allow for type checking using static analysis. Instead, prefer using pydantic classes, which allows you to easily specify data structures.
- **Documentation:** All code should be documented (we will use the Google docstring standard). This will be enforced by linting.

## Deployment

The backend works with a postgres database. Once set up, this database needs some tables. You can bootstrap the database using [this sript](./create_tables.sql).

Once this backend database is set up, Connex needs information on how to connect to it. therefore, add a database.ini in [./zeno_backend/database](./zeno_backend/database/) as follows:

```
[postgresql]
host=[whereever your DB is running]
dbname=[the name of your DB]
user=[usename for DB login]
password=[password for DB login]
```

Then, the backend can be started with poetry, from within the backend folder, run: `poetry run backend`
