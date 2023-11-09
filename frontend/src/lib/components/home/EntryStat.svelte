<script lang="ts">
	import { tooltip } from '$lib/util/tooltip';
	import { shortenNumber } from '$lib/util/util';

	export let icon: string;
	export let text: string | number;
	export let tooltipContent: string;
</script>

<div class="mx-2 flex items-center text-grey-dark" use:tooltip={{ text: tooltipContent }}>
	<div class="mr-2 h-6 w-6">
		<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-dark">
			<path d={icon} />
		</svg>
	</div>
	{typeof text === 'number' ? shortenNumber(text, 1) : text}
</div>
