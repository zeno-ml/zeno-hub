<script lang="ts">
	import Paper from '@smui/paper';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	let paperHeight;
</script>

<button
	class="absolute inset-0 z-20 flex items-baseline justify-center bg-grey bg-opacity-60 p-12 text-left"
	transition:fade={{ duration: 200 }}
	bind:clientHeight={paperHeight}
	on:mousedown={() => dispatch('close')}
	on:keydown={() => undefined}
>
	<Paper class="flex flex-col pt-3" elevation={7} on:mousedown={(e) => e.stopPropagation()}>
		<slot />
	</Paper>
</button>
