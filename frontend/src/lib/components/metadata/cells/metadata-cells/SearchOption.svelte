<script lang="ts">
	import { tooltip } from '$lib/util/tooltip';

	export let highlighted: boolean;
	export let id: string;
	export let tooltipContent: string;
</script>

<button
	{id}
	class={`flex h-7 cursor-pointer items-center pb-1 pl-2 pr-2 pt-1  ${
		highlighted ? 'bg-primary-mid' : 'hover:bg-yellowish'
	}`}
	on:click
	use:tooltip={{
		text: tooltipContent
	}}
>
	<slot />
</button>
