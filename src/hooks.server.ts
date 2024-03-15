import { dev } from "$app/environment";

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	if (dev && event.url.pathname.startsWith("/api")) {
		return Response.redirect(new URL(`http://127.0.0.1:8000${event.url.pathname}`), 302);
	}

	const response = await resolve(event);
	return response;
}
