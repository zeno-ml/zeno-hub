# Development

Before working on Zeno, please carefully read this document.

## Architecture Overview

Zeno is comprised of several subsystems.

Zeno's frontend is a SvelteKit application (`frontend/`).

Zeno's backend is a Python FastAPI server (`backend/`). The backend stores and serves all project data for Zeno's frontend.

There can exist multiple backends that the frontend talks to. To orchestrate between the Zeno frontend and the backends that are available to it, a third service exists (`connex/`), which is also a Python FastAPI server.

For the frontend we used the compiled OpenAPI interface instead of raw `fetch` requests to interact with the backend and connex.
The API can be generated using the `npm run generate-api` and `npm run generate-connex-api` commands, respectively.
These commands create the `frontend/src/lib/zenoapi` and `frontend/src/lib/connexapi` folders (must be run while server is running).
All the TypeScript classes that refer to server functionality used in the frontend come from the compiled OpenAPI spec, giving us a single source of truth for classes from Python.

## Development Installation

After cloning the repository:

- Install [`Poetry`](https://python-poetry.org/docs/master/#installing-with-the-official-installer), [`nodejs`](https://nodejs.org/en/download/) and use [`VSCode`](https://code.visualstudio.com/) as your editor.

We suggest you install the following VSCode extensions:

- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Svelte for VSCode](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode)

Since we use different python environments for connex and the backend, linting etc. might not work correctly if this root folder of our projects is opened in VSCode.
To work around this, open the `zeno.code-workspace` in this folder. Then, run connex, frontend, and backend as described in their respective README files.

## Making a release

Refer to the DEVELOPMENT.md files in the respective Zeno subsystem that you would like to release.
