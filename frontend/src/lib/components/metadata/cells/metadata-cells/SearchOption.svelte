<script lang="ts">
	import { tooltip } from '@svelte-plugins/tooltips';

	export let highlighted: boolean;
	export let id: string;
	export let tooltipContent: string;
</script>

<button
	{id}
	class={`flex items-center pt-1 pb-1 pl-2 pr-2 h-7 cursor-pointer  ${
		highlighted ? 'bg-primary-mid' : 'hover:bg-yellowish'
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
