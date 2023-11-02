<script lang="ts">
	import SliceDetails from '$lib/components/general/SliceDetails.svelte';
	import type { Slice } from '$lib/zenoapi';

	export let sli: Slice | undefined;

	let showTooltip = false;
</script>

{#if sli !== undefined}
	<div
		class="cursor-default text-primary"
		role="tooltip"
		on:mouseover={() => (showTooltip = true)}
		on:mouseout={() => (showTooltip = false)}
		on:focus={() => (showTooltip = true)}
		on:blur={() => (showTooltip = false)}
	>
		{sli.sliceName}
	</div>
	{#if sli.sliceName !== 'All Instances' && showTooltip}
		<div class="absolute z-10">
			<div class="rounded-lg bg-background p-2.5 shadow-xl">
				<SliceDetails predicateGroup={sli.filterPredicates} />
			</div>
		</div>
	{/if}
{/if}
