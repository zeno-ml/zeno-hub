<script lang="ts">
	import Button from '@smui/button/src/Button.svelte';
	import Paper, { Content } from '@smui/paper';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	export let message: string;
	export let confirmText = 'Confirm';
	export let cancelText = 'Cancel';

	const dispatch = createEventDispatcher();

	let paperHeight;
</script>

<div
	class="fixed inset-0 z-20 flex justify-center items-baseline p-12 bg-grey bg-opacity-60"
	transition:fade={{ duration: 200 }}
	bind:clientHeight={paperHeight}
>
	<Paper class="p-6 flex flex-col" elevation={7}>
		<Content>
			<div class="mb-4">{message}</div>
			<slot />
			<div class="flex m-auto justify-center">
				<Button style="margin-right: 10px" variant="outlined" on:click={() => dispatch('cancel')}>
					{cancelText}
				</Button>
				<Button
					style="margin-right: 10px"
					variant="unelevated"
					on:click={() => dispatch('confirm')}
				>
					{confirmText}
				</Button>
			</div>
		</Content>
	</Paper>
</div>
