# Development

Before working on Zeno, please carefully read this document.

## Architecture Overview

Zeno is comprised of two subsystems.

Zeno's frontend is a SvelteKit application (`frontend/`).

Zeno's backend is a Python FastAPI server (`backend/`). The backend stores and serves all project data for Zeno's frontend.

For the frontend we used the compiled OpenAPI interface instead of raw `fetch` requests to interact with the backend.
The API can be generated using the `npm run generate-api` command.
These commands create the `frontend/src/lib/zenoapi` folder (must be run while server is running).
All the TypeScript classes that refer to server functionality used in the frontend come from the compiled OpenAPI spec, giving us a single source of truth for classes from Python.

## Development Installation

After cloning the repository:

- Install [`Poetry`](https://python-poetry.org/docs/master/#installing-with-the-official-installer), [`nodejs`](https://nodejs.org/en/download/) and use [`VSCode`](https://code.visualstudio.com/) as your editor.

We suggest you install the VSCode extensions as specified in `.vscode/extensions.json`.

To make python linting work correctly, we suggest issuing `poetry config virtualenvs.in-project true` to make poetry create a virtualenv in the backend project.
In vscode, you can then select this venv as the used Python interpreter.

## Making a release

Refer to the DEVELOPMENT.md files in the respective Zeno subsystem that you would like to release.
