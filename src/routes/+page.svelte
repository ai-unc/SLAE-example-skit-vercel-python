<script lang="ts">
	import { dev } from "$app/environment";
	import { Circle, CircleCheckBig, Play } from "lucide-svelte";
	import { onMount } from "svelte";

	let text = $state<string>();
	type Todo = { id: number; text: string; completed: boolean };
	let todos: Array<Todo> = $state([]);
	let selected_todo: Todo | null = $state(null);

	onMount(() => {
		(async () => {
			await getTodos();
		})();
	});

	async function ping() {
		const response = await fetch("/api/ping");
		if (response.ok) {
			const response_json = await response.json();
			text = response_json.ping;
		} else console.error(`Error: ${response.status}`);
	}
	async function getTodos() {
		const response = await fetch("/api/getTodos");
		if (response.ok) {
			const response_json = await response.json();
			todos = response_json;
		} else console.error(`Error: ${response.status}`);
	}
	async function completeTodo() {
		// HACK: POST/DELETE methods don't work with hooks redirect solution currently
		const origin = dev ? "http://127.0.0.1:8000" : "";
		const response = await fetch(`${origin}/api/completeTodo`, {
			method: "POST",
			body: JSON.stringify(selected_todo),
			headers: {
				"Content-Type": "application/json",
			},
		});
		if (response.ok) {
			const response_json = await response.json();
			todos.find((todo) => todo.id === response_json.id)!.completed = true;
		} else console.error(`Error: ${response.status}`, await response.json());
	}
	async function deleteTodo() {
		const id = selected_todo!.id;
		// HACK: POST/DELETE methods don't work with hooks redirect solution currently
		const origin = dev ? "http://127.0.0.1:8000" : "";
		const response = await fetch(`${origin}/api/deleteTodo`, {
			method: "DELETE",
			body: JSON.stringify(selected_todo),
			headers: {
				"Content-Type": "application/json",
			},
		});
		if (response.ok) {
			selected_todo = null;
			const i = todos.findIndex((todo) => todo.id === id);
			todos.splice(i, 1);
		} else console.error(`Error: ${response.status}`, await response.json());
	}
</script>

<main>
	<h1>SLAE Example SKit & Python App via Vercel Functions</h1>

	<div class="endpoints">
		<div class="endpoint" onfocusout={() => (text = undefined)}>
			<div class="label">
				<div class="http_verb get">GET</div>
				<div class="path">/api/ping</div>
				<div class="description">Replies with "pong!" or "pong"</div>
				<button onclick={ping}><Play class="icon" /></button>
			</div>
			{#if text}
				<div class="response"><strong>Response:</strong> {text}</div>
			{/if}
		</div>
		<div class="endpoint">
			<div class="label">
				<div class="http_verb get">GET</div>
				<div class="path">/api/getTodos</div>
				<div class="description">Fetches Todos</div>
				<button onclick={getTodos}><Play class="icon" /></button>
			</div>
		</div>
		<div class="endpoint">
			<div class="label">
				<div class="http_verb post">POST</div>
				<div class="path">/api/completeTodo</div>
				<div class="description">Marks a Todo Complete</div>
				<button onclick={completeTodo} disabled={selected_todo === null || selected_todo.completed}><Play class="icon" /></button>
			</div>
		</div>
		<div class="endpoint">
			<div class="label">
				<div class="http_verb delete">DELETE</div>
				<div class="path">/api/deleteTodo</div>
				<div class="description">Deletes a Todo</div>
				<button onclick={deleteTodo} disabled={selected_todo === null}><Play class="icon" /></button>
			</div>
		</div>
	</div>

	<div class="todos">
		<h2>Todos</h2>
		{#each todos as todo}
			<button class="todo" class:selected={selected_todo === todo} onclick={() => (selected_todo === todo ? (selected_todo = null) : (selected_todo = todo))}>
				{todo.text}

				{#if todo.completed}
					<CircleCheckBig />
				{:else}
					<Circle />
				{/if}
			</button>
		{/each}
	</div>
</main>

<style lang="postcss">
	main {
		overflow: hidden;
		@apply mx-2 max-w-full;
		@apply sm:mx-4;
		@apply lg:mx-auto lg:w-4/5;
	}
	h1 {
		@apply text-center font-semibold;

		@apply my-2 text-xs;
		@apply sm:mt-4 sm:text-lg;
		@apply lg:my-2 lg:text-6xl;
	}

	.endpoints {
		@apply flex flex-col items-center;

		@apply gap-y-1;
		@apply sm:my-[20px] sm:gap-y-2;
		@apply lg:my-[40px] lg:gap-y-3;

		.endpoint {
			@apply w-full bg-gray-100;
			@apply rounded-md border border-solid;

			@apply p-1;
			@apply lg:p-2;

			&:has(.http_verb.get) {
				@apply border-blue-500;
			}
			&:has(.http_verb.post) {
				@apply border-yellow-300;
			}
			&:has(.http_verb.delete) {
				@apply border-red-500;
			}

			.label {
				@apply flex items-center gap-x-2;

				.http_verb {
					@apply rounded font-semibold text-white;

					@apply p-1 text-sm;
					@apply sm:p-[0.3rem];
					@apply lg:p-2 lg:text-lg;

					&.get {
						@apply bg-blue-500;
					}
					&.post {
						@apply bg-yellow-300;
					}
					&.delete {
						@apply bg-red-500;
					}
				}

				.path {
					@apply font-medium;

					@apply text-[10px];
					@apply sm:text-xs;
					@apply lg:text-lg;
				}

				.description {
					@apply font-light text-gray-500;

					@apply text-[8px];
					@apply sm:text-[10px];
					@apply lg:text-sm;
				}

				button {
					@apply ml-auto flex items-center justify-center;
					@apply rounded-xl bg-gray-800 text-gray-200;

					@apply mr-1 square-8;
					@apply lg:mr-4 lg:square-12;

					:global(.icon) {
						width: 80%;
						height: 80%;
					}

					&:disabled {
						@apply cursor-not-allowed opacity-50;
					}
				}
			}

			.response {
				@apply mt-1 text-xs;
				@apply sm:text-sm;
				@apply lg:mt-2 lg:text-sm;
			}
		}
	}

	.todos {
		@apply flex flex-col;

		@apply mx-2 my-2 gap-y-2;
		@apply lg:gap-y-4;

		h2 {
			@apply text-center font-medium;

			@apply text-2xl;
			@apply sm:text-3xl;
			@apply lg:text-5xl;
		}

		.todo {
			@apply rounded-sm bg-gray-100;
			@apply flex items-center justify-between;

			@apply h-10 p-1 text-xs;
			@apply sm:h-16 sm:px-2 sm:text-sm;
			@apply lg:px-4 lg:py-2 lg:text-lg;

			&.selected {
				@apply ring-2 ring-red-800;
			}
		}
	}
</style>
