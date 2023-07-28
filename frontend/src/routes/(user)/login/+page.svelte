<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;
</script>

<form
	class="flex flex-col items-center justify-center bg-background p-12 rounded-xl"
	method="POST"
	action="?/login"
	use:enhance
>
	<div class="flex flex-col items-center">
		<Textfield input$name="username" label="Username" value={form ? form.username : ''} />
		<Textfield
			type="password"
			input$name="password"
			value={form ? form.password : ''}
			label="Password"
		/>
		<Button type="submit">Login</Button>
	</div>
	<div>
		Don't have an account? <a href="/signup">Sign up now!</a>
	</div>
	{#if form?.error}
		<p>
			{form.error}
			{#if form.showReset}
				<a href="/forgot">Forgot your password?</a>
			{/if}
		</p>
	{/if}
</form>
