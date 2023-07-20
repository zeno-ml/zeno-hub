<script lang="ts">
	import type { User } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let user: User;
</script>

<div class="horizontal">
	<form method="POST" action="?/updateUser">
		<Textfield
			input$name="name"
			label="Username"
			bind:value={user.name}
			style="margin-right: 40px;"
		/>
		<Textfield label="Email" value={user.email} disabled style="margin-right: 40px;" />
		<Button type="submit" variant="raised">Update</Button>
	</form>
</div>

<style>
	.horizontal {
		display: flex;
		align-items: center;
	}
</style>
