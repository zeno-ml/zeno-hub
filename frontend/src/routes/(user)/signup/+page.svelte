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
		<Textfield input$name="username" value={form ? `${form.name}` : ''} label="User name" />
		<Textfield
			input$name="email"
			type="email"
			value={form ? `${form.email}` : ''}
			label="Email address"
		/>
		<Textfield
			input$name="password"
			type="password"
			value={form ? `${form.password}` : ''}
			label="Password"
		/>
		<Textfield
			input$name="repeatPassword"
			type="password"
			value={form ? `${form.repeat}` : ''}
			label="Repeat password"
		/>
		<Button type="submit">Sign Up</Button>
		<div>
			Already have an account? <a href="/login">Log in now!</a>
		</div>
		{#if form?.error}
			<p>{form.error}</p>
		{/if}
	</div>
</form>
