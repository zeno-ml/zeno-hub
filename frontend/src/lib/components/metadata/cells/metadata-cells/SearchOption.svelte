<script lang="ts">
	import { tooltip } from '@svelte-plugins/tooltips';

	export let highlighted: boolean;
	export let id: string;
	export let tooltipContent: string;
</script>

<button
	{id}
	class={`flex items-center p-1 h-6 cursor-pointer hover:bg-yellowish ${
		highlighted ? 'bg-primary-mid' : ''
	}`}
	on:click
	use:tooltip={{
		content: tooltipContent,
		theme: 'zeno-tooltip',
		autoPosition: true
	}}
>
	<slot />
</button>
