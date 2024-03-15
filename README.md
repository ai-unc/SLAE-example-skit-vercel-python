# SLAE Example SKit & Python App via Vercel Functions

An example application showing how to use a python backend runtime with a SvelteKit application.

Vercel provides a [Python runtime](https://vercel.com/docs/functions/runtimes/python) for their serverless functions, which can be declared in the root of the project in the [`api`](/api) directory.

The SvelteKit `api` directory within the `src/routes` path is [incompatible with this approach](https://kit.svelte.dev/docs/adapter-vercel#notes-vercel-functions), but that suits our needs just fine.

During development, the Python server will be running at 127.0.0.1:8000, meaning any requests to origin/api would normally fail. SvelteKit [`hooks.server.ts`](/src/hooks.server.ts) will reroute these requests during development to the appropriate address. **Note:** POST and DELETE requests currently don't work locally with this solution, origin must be injected manually.

The Python server uses [FastAPI](https://github.com/tiangolo/fastapi), but in theory any implementation or library would work. All implementation is using runtime memory, there is no database to persist data.

There may be a more optimal file setup for maintainability.
