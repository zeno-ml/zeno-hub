<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import Textfield from '@smui/textfield';

	export let form;

	let agreed = false;
</script>

<svelte:head>
	<title>Register</title>
</svelte:head>

<form
	class="flex flex-col items-center justify-center rounded-xl bg-background p-12"
	method="POST"
	action="?/signup"
	use:enhance
>
	<div class="flex flex-col items-center">
		<a href="/">
			<img src="/zeno-logo.png" alt="Zeno logo" width="200px" class="mb-5" />
		</a>

		<Textfield
			input$name="username"
			value={form ? `${form.name}` : ''}
			label="User name"
			class="mb-3 w-56"
		/>
		<Textfield
			input$name="email"
			type="email"
			value={form ? `${form.email}` : ''}
			label="Email address"
			class="mb-3 w-56"
		/>
		<Textfield
			input$name="password"
			type="password"
			value={form ? `${form.password}` : ''}
			label="Password"
			class="mb-3 w-56"
		/>
		<Textfield
			input$name="repeatPassword"
			type="password"
			value={form ? `${form.repeat}` : ''}
			label="Repeat password"
			class="mb-3 w-56"
		/>
		{#if form?.error}
			<p class="text-error mt-4 font-semibold">{form.error}</p>
		{/if}
		<p class="mt-2 w-64 text-center">
			Password must be at least 8 characters long and have at least one number, one special
			character, and one uppercase letter.
		</p>
		<div class="mt-4 flex items-center">
			<Checkbox bind:checked={agreed} />
			<span>
				By signing up you agree to our <a
					href="/tos"
					target="_blank"
					class="text-primary visited:text-primary hover:underline">Terms of Service</a
				>.</span
			>
		</div>
		<Button type="submit" variant="raised" class="mt-5" disabled={!agreed}>Sign Up</Button>
		<p class="mt-5">
			Already have an account? <a href="/" class="text-primary visited:text-primary hover:underline"
				>Log in now!</a
			>
		</p>
	</div>
</form>
