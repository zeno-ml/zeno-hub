<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	let username = '';
</script>

<svelte:head>
	<title>Reset Password</title>
</svelte:head>

<form
	method="POST"
	class="flex flex-col items-center justify-center bg-background p-12 rounded-xl"
	action="?/code"
	use:enhance
>
	<div class="flex flex-col items-center">
		<Textfield input$name="username" bind:value={username} label="Username" />
		<Button type="submit" disabled={username.length === 0}>Confirm</Button>
	</div>
</form>
