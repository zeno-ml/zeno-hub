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
		<span>
			Hi {data.username}, please enter the verification code that we sent to you.
		</span>
		<Textfield input$name="code" label="Verification Code" value={form ? `${form.code}` : ''} />
		<Button type="submit">Verify</Button>
	</div>
	{#if form?.error}
		<p>{form.error}</p>
	{/if}
</form>
