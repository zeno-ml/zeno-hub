# Development

Before working on Zeno, please carefully read this document.

## Development Setup

This is our overall development setup for Zeno. Individual parts in this repository might have their own `DEVELOPMENT.md`.

### Most Importantly

We’re all in this together to quickly make something great. And let’s have fun while we’re doing it. The guidelines below are to help us achieve this goal, but if there’s anything that doesn’t feel right to you, bring it up with your co-workers or supervisor and we’ll discuss and modify these guidelines as necessary.

### Tenets

- **Use Automatic Static Analysis:** All code should be automatically tested, including formatting, linting, and typechecking. Any problems that are caught by static analysis before runtime or review save time and frustration.
- **Don’t Skimp on Unit/Integration/End-to-end Testing:** We should strive to cover our code with tests (to the extent reasonable). In particular, writing a quick test to demonstrate the expected behavior of new functions, or to test behavior when fixing bugs is highly encouraged.
  Fast, Rigorous Code Review: All code should be reviewed before being checked in. Rapid code reviews should be prioritized, as others may be blocked if they are waiting for review for a long time.
- **Small Commits:** We should strive for [small pull requests](https://www.swarmia.com/blog/why-small-pull-requests-are-better/), as they are easier to check rigorously.
  Continuous Deployment: Once code is checked in (for an already-live service), it will be considered basically production ready and may be deployed at any time. We can use feature flags to have code that is checked in but not enabled, which also enables gradual releases and A/B testing.
  -- **Monorepo:** As much as possible, we will store all code in a single repo. This [removes the necessity for reconciling different versions of software](https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/fulltext), which can become a major source of overhead as things grow larger.

### Infrastructure

#### Local Checking:

git pre-commit

#### Continuous Integration/Deployment:

Performed through Github Actions

#### Hardware Provisioning:

AWS, managed by Terraform

### GitHub

We use GitHub to manage our code. As mentioned above, all our code is in one single repository. This means we need some housekeeping rules to maintain a clear, understandable repository structure:

1. `main` is only for production-ready code: If you are implementing new features, create a new branch. To keep some overview of the branches we have, name your branch according to `[your name]/[what your branch does]`. Once ready for release, create a PR to merge your branch back into `main`.
2. Use conventional commits: We use conventional commits both to make our commits easier to understand and to automate deployment. There are many good tools to help you with this, for example [commitizen](https://commitizen-tools.github.io/commitizen/), which you can install via [homebrew](https://formulae.brew.sh/formula/commitizen).

## Architecture Overview

Zeno is comprised of two subsystems.

Zeno's frontend is a SvelteKit application (`frontend/`).

Zeno's backend is a Python FastAPI server (`backend/`). The backend stores and serves all project data for Zeno's frontend.

For the frontend we used the compiled OpenAPI interface instead of raw `fetch` requests to interact with the backend.
The API can be generated using the `npm run generate-api` command.
These commands create the `frontend/src/lib/zenoapi` folder (must be run while server is running).
All the TypeScript classes that refer to server functionality used in the frontend come from the compiled OpenAPI spec, giving us a single source of truth for classes from Python.

## Development Installation

The recommended way to locally develop is to use `Docker` and `docker-compose`. We still recommend you install the frontend and backend locally to enable linting and testing.

1. We recommend you use [`VSCode`](https://code.visualstudio.com/) as your editor.
2. Install [`Docker`](https://docs.docker.com/get-docker/), [`npm`](https://www.npmjs.com/get-npm), and [`poetry`](https://python-poetry.org/docs/#installation).
3. Install the frontend with `npm install` in the `frontend/` directory.
4. Get the variables to create a `.env` file in the frontend folder.
5. Configure Poetry to make local virtualenv with `poetry config virtualenvs.in-project true`. You can select this as the Python interpreter in VSCode.
6. Install the backend with `poetry install` in the `backend/` directory.
7. We suggest you install the VSCode extensions as specified in `.vscode/extensions.json`.
8. Run `docker-compose up -d` in the root directory to start the backend and frontend servers.
9. Navigate to `localhost:5173` to start using Zeno. Any changes you make to the frontend will be live-reloaded. Changes to the backend will require restarting the server with `docker-compose restart backend`.

## Making a release

Refer to the DEVELOPMENT.md files in the respective Zeno subsystem that you would like to release.
It is best to deploy [Zeno's backend](./backend/DEVELOPMENT.md#deployment) first, then deploy the [frontend](./frontend/DEVELOPMENT.md#deployment).

## Building docker images on ECS

You can build docker images on Amazon ECS using the included `buildspec.yml` file.
To do so, you need to have the following environment variables set:
- AWS_ACCOUNT_ID: Your account ID
- AWS_REGION: The region you're building in
- DOCKER_USERNAME: A username for docker to pull docker images
- DOCKER_PASSWORD: The password for the username
