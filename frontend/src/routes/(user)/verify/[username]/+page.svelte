<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button';
	import Textfield from '@smui/textfield';

	export let form;
	export let data;
</script>

<form
	class="flex flex-col items-center justify-center rounded-xl bg-background p-12"
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
			class="mb-3 w-56"
		/>
		<Button type="submit" variant="raised" class="mt-3">Verify Account</Button>
	</div>
	{#if form?.error}
		<p class="font-semibold text-error">{form.error}</p>
	{/if}
</form>
