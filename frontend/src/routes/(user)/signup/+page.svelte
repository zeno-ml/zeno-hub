<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;
</script>

<svelte:head>
	<title>Register</title>
</svelte:head>

<form
	class="flex flex-col items-center justify-center bg-background p-12 rounded-xl"
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
			class="w-56 mb-3"
		/>
		<Textfield
			input$name="email"
			type="email"
			value={form ? `${form.email}` : ''}
			label="Email address"
			class="w-56 mb-3"
		/>
		<Textfield
			input$name="password"
			type="password"
			value={form ? `${form.password}` : ''}
			label="Password"
			class="w-56 mb-3"
		/>
		<Textfield
			input$name="repeatPassword"
			type="password"
			value={form ? `${form.repeat}` : ''}
			label="Repeat password"
			class="w-56 mb-3"
		/>
		<Button type="submit" variant="raised" class="mt-5">Sign Up</Button>
		<p class="mt-5">
			Already have an account? <a href="/">Log in now!</a>
		</p>
		{#if form?.error}
			<p>{form.error}</p>
		{/if}
	</div>
</form>
