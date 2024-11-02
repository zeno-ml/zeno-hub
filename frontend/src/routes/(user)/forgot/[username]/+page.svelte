<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button';
	import Textfield from '@smui/textfield';

	export let form;
</script>

<svelte:head>
	<title>Reset Password</title>
</svelte:head>

<form
	method="POST"
	class="flex flex-col items-center justify-center rounded-xl bg-background p-12"
	action="?/reset"
	use:enhance
>
	<img src="/zeno-logo.png" alt="Zeno logo" width="200px" class="mb-5" />
	<div class="mb-3">Please check your email for a verification code to reset your password.</div>
	<div class="flex flex-col items-center">
		<Textfield
			input$name="validation"
			value={form ? `${form.validation}` : ''}
			label="Verification code"
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
			label="Confirm password"
			class="mb-3 w-56"
		/>
		<Button type="submit" variant="raised" class="mt-5">Reset</Button>
		{#if form?.error}
			<p class="mt-5 text-center font-semibold text-error">
				{form.error}
			</p>
		{/if}
	</div>
</form>
