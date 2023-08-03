<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;
</script>

<svelte:head>
	<title>Reset Password</title>
</svelte:head>

<form
	method="POST"
	class="flex flex-col items-center justify-center bg-background p-12 rounded-xl"
	action="?/reset"
	use:enhance
>
	<div>We have sent you a validation code to reset your password.</div>
	<div class="flex flex-col items-center">
		<Textfield
			input$name="validation"
			value={form ? `${form.validation}` : ''}
			label="Validation code"
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
		<Button type="submit">Reset</Button>
		{#if form?.error}
			<p>{form.error}</p>
		{/if}
	</div>
</form>
