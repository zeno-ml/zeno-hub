<script lang="ts">
	import { tooltip } from '$lib/util/tooltip';
	import { shortenNumber } from '$lib/util/util';
	import { Icon } from '@smui/button';

	export let entryType: 'project' | 'report';
	export let icon: string;
	export let text: string | number;
	export let tooltipContent: string;
</script>

<div
	class="ml-8 flex items-center {entryType === 'report' ? 'text-white' : 'text-grey'} font-semibold"
	use:tooltip={{ text: tooltipContent }}
>
	<div class="mr-2 h-6 w-6 {entryType === 'report' ? 'fill-white' : 'fill-grey'} ">
		<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
			<path d={icon} />
		</Icon>
	</div>
	{typeof text === 'number' ? shortenNumber(text, 1) : text}
</div>
