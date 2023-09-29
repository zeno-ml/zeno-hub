<script lang="ts">
	import { getMetricsForSlices } from '$lib/api/slice';
	import { metric } from '$lib/stores';
	import type { Slice } from '$lib/zenoapi';

	export let compare: boolean;
	export let slice: Slice;
	export let sliceModel: string;
</script>

{#await getMetricsForSlices( [{ slice: slice, model: sliceModel, metric: $metric ? $metric.id : -1 }] ) then res}
	{#if res !== null}
		<button class={compare ? 'flex flex-col items-center mr-2.5 text-xs ' : 'flex items-center'}>
			<span class="{!compare ? 'mr-2.5' : ''} text-right">
				{res[0].metric !== undefined && res[0].metric !== null ? res[0].metric.toFixed(2) : ''}
			</span>
			<span class="{!compare ? 'mr-1' : ''} text-right italic text-grey-dark">
				({res[0].size.toLocaleString()})
			</span>
		</button>
	{/if}
{/await}
