<script lang="ts">
	import { browser } from '$app/environment';
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;

	let redirect = '';
	if (browser) {
		const urlParams = new URLSearchParams(window.location.search);
		redirect = urlParams.get('redirect') ?? '';
	}
</script>

<form
	class="flex flex-col items-center justify-center rounded-xl bg-background p-12"
	method="POST"
	action="?/login"
	use:enhance
>
	<div class="flex flex-col items-center">
		<input type="hidden" name="redirect" value={redirect} />
		<a href="/">
			<img src="/zeno-logo.png" alt="Zeno logo" width="200px" class="mb-5" />
		</a>
		<Textfield
			input$name="username"
			label="Username"
			value={form ? form.username : ''}
			class="mb-3 w-56"
		/>
		<Textfield
			type="password"
			input$name="password"
			value={form ? form.password : ''}
			label="Password"
			class="w-56"
		/>
		<Button type="submit" variant="raised" class="mt-5">Login</Button>
		{#if form?.error}
			<p class="mt-5 text-center font-semibold text-error">
				{form.error}
				{#if form.showReset}
					<br />
					<a href="/forgot" class="text-primary">Reset your password?</a>
				{/if}
			</p>
		{/if}
		<p class="mt-7">
			Don't have an account? <a href="/signup/" class="text-primary">Sign up now!</a>
		</p>
	</div>
</form>
