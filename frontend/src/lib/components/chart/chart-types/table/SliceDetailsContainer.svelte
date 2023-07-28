<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import SliceDetails from '$lib/components/general/SliceDetails.svelte';
	import { selections } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import type { Slice } from '$lib/zenoapi';

	export let sli: Slice | undefined;

	let showTooltip = false;
</script>

{#if sli !== undefined}
	<div
		class="text-primary cursor-pointer"
		on:click={() => {
			selections.update((sel) => ({
				slices: sli !== undefined && sli.sliceName !== 'All Instances' ? [sli.id] : [],
				metadata: sel.metadata,
				tags: sel.tags
			}));
			goto(`${getProjectRouteFromURL($page.url)}/explore`);
		}}
		on:mouseover={() => (showTooltip = true)}
		on:mouseout={() => (showTooltip = false)}
		on:focus={() => (showTooltip = true)}
		on:blur={() => (showTooltip = false)}
		on:keydown={() => ({})}
	>
		{sli.sliceName}
	</div>
	{#if sli.sliceName !== 'All Instances' && showTooltip}
		<div class="z-10 absolute">
			<div class="bg-background p-2.5 rounded-lg shadow-xl">
				<SliceDetails predicateGroup={sli.filterPredicates} />
			</div>
		</div>
	{/if}
{/if}
