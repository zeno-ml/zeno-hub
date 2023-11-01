<script lang="ts">
	import { getMetricsForSlices } from '$lib/api/slice';
	import { metric } from '$lib/stores';
	import type { Slice, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let compare: boolean;
	export let slice: Slice;
	export let sliceModel: string;

	const zenoClient = getContext('zenoClient') as ZenoService;

	$: result = getMetricsForSlices(
		[{ slice: slice, model: sliceModel, metric: $metric ? $metric.id : -1 }],
		zenoClient
	);
</script>

{#await result then res}
	{#if res !== null}
		<button class={compare ? 'mr-2.5 flex flex-col items-center text-xs ' : 'flex items-center'}>
			<span class="{!compare ? 'mr-2.5' : ''} text-right">
				{res[0].metric !== undefined && res[0].metric !== null ? res[0].metric.toFixed(2) : ''}
			</span>
			<span class="{!compare ? 'mr-1' : ''} text-right italic text-grey-dark">
				({res[0].size.toLocaleString()})
			</span>
		</button>
	{/if}
{/await}
