<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let form;
	export let data;
</script>

<form
	class="flex flex-col items-center justify-center bg-background p-12 rounded-xl"
	method="POST"
	action="?/verify"
	use:enhance
>
	<div class="flex flex-col items-center">
		<a href="/">
			<img src="/zeno-logo.png" alt="Zeno logo" width="200px" class="mb-5" />
		</a>
		<p>
			Welcome {data.username}! please enter the verification code below.
		</p>
		<Textfield
			input$name="code"
			label="Verification Code"
			value={form ? `${form.code}` : ''}
			class="w-56 mb-3"
		/>
		<Button type="submit" variant="raised" class="mt-3">Verify Account</Button>
	</div>
	{#if form?.error}
		<p>{form.error}</p>
	{/if}
</form>
