<script lang="ts">
	import SliceDetails from '$lib/components/general/SliceDetails.svelte';
	import type { Slice } from '$lib/zenoapi';

	export let sli: Slice | undefined;

	let showTooltip = false;
</script>

{#if sli !== undefined}
	<div
		class="text-primary cursor-default"
		on:mouseover={() => (showTooltip = true)}
		on:mouseout={() => (showTooltip = false)}
		on:focus={() => (showTooltip = true)}
		on:blur={() => (showTooltip = false)}
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
