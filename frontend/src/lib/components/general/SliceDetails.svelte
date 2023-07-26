<script lang="ts">
	import type { FilterPredicateGroup } from '$lib/zenoapi';
	import MetaChip from './MetaChip.svelte';

	export let predicateGroup: FilterPredicateGroup;
</script>

<div class="flex flex-wrap">
	{#each predicateGroup.predicates as pred, i}
		{#if 'predicates' in pred}
			{#if i !== 0}
				<MetaChip content={pred.join} />
			{/if}
			<MetaChip content={'('} />
			<svelte:self predicateGroup={pred} />
			<MetaChip content={')'} />
		{:else}
			{#if i !== 0}
				<MetaChip content={pred.join} />
			{/if}
			<MetaChip
				content={pred.column.name +
					pred.operation +
					`${
						!isNaN(Number(pred.value)) && typeof pred.value !== 'boolean'
							? Number(pred.value).toFixed(2)
							: pred.value
					}`}
			/>
		{/if}
	{/each}
</div>
