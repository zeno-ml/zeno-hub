<script lang="ts">
	import Button from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	export let message: string;
	export let confirmText = 'Confirm';
	export let cancelText = 'Cancel';

	const dispatch = createEventDispatcher();
</script>

<div
	class="fixed inset-0 z-20 flex items-baseline justify-center bg-grey bg-opacity-60 p-12"
	transition:fade={{ duration: 200 }}
>
	<Paper class="flex flex-col p-6" elevation={7}>
		<Content>
			<div class="mb-4">{message}</div>
			<slot />
			<div class="m-auto flex justify-end">
				<Button style="margin-right: 10px" variant="outlined" on:click={() => dispatch('cancel')}>
					{cancelText}
				</Button>
				<Button style="margin-right: 10px" variant="outlined" on:click={() => dispatch('confirm')}>
					{confirmText}
				</Button>
			</div>
		</Content>
	</Paper>
</div>
