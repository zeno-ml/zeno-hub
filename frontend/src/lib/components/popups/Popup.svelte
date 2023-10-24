<script lang="ts">
	import Paper from '@smui/paper';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	let paperHeight;
</script>

<button
	class="absolute inset-0 z-20 flex justify-center items-baseline p-12 bg-grey bg-opacity-60"
	transition:fade={{ duration: 200 }}
	bind:clientHeight={paperHeight}
	on:mousedown={() => dispatch('close')}
	on:keydown={() => undefined}
>
	<Paper class="pt-3 flex flex-col" elevation={7} on:mousedown={(e) => e.stopPropagation()}>
		<slot />
	</Paper>
</button>
