# Development

Zeno's frontend is a SvelteKit application.

## Development Setup

**Note:** We recommend you use Docker as detailed in the [overall development setup](../DEVELOPMENT.md) instead of setting this up locally.

Before starting local development, you need a `.env` file.
You can take inspiration for this from the `.env.example` file in this folder.
Once you have this set up, you can run `yarn` or `npm install` to install required npm packages and then `yarn dev` or `npm run dev` to run the frontend in dev mode.

When you add a new route to the backend, run `npm run generate-api` to update the functions in the `ZenoService` object.

### Static Analysis Tools

eslint (linting), prettier (formatting)

### Testing

Vitest

### Guidelines:

- **Organize your Code:** We use the SvelteKit code organization pattern with some added conventions. This means any routes go into [/routes](./src/routes/) and all reusable code goes into [/lib](./src/lib/). In [/lib](./src/lib/), we have [/components](./src/lib/components/) for svelte components that we reuse, [/util](./src/lib/util/) for utility functions, [/api](./src/lib/api/) for web request wrappers, and an [api folder](./src/lib/zenoapi/) for our backend connection.
- **No use of `any`:** Do not use the `any` type in your TypeScript code if it can be prevented. If you really don’t know the type of your variable, [prefer `unknown` over `any`](https://github.com/Microsoft/TypeScript/pull/24439).
- **Componentize:** Typescript, but especially Svelte files (because they include TS, HTML, and CSS code) are very hard to understand, review, and extend if they contain too much code. Thus, make your your components [serve a single, obvious purpose](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Svelte_components).
- **Comment your Code:** Your linter will force you to add [JSDoc comments](https://jsdoc.app/). However, this does not mean you can’t add additional documentation to complex algorithms or hard to understand code segments.

Everything else should be handled by linting and typechecking. If your code does not pass CI, it will not be reviewed. This makes it much easier for everyone to do rigorous and quick code reviews.

## Deployment

To inform the frontend about where your backend has been deployed, set an environment variable witht the name `PUBLIC_BACKEND_ENDPOINT`.
Then build the project by issuing `yarn build` or `npm run build` depending on which package manager you use.
This will create a build folder that can be started as a node server (e.g., `node build`).
