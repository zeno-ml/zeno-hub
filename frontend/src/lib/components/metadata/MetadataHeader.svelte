<script lang="ts">
	import { page } from '$app/stores';
	import {
		columns,
		comparisonColumn,
		comparisonModel,
		metric,
		metrics,
		model,
		models
	} from '$lib/stores';

	let comparisonColumnOptions = $columns.filter((c) => c.model === $model);
	if (!$comparisonColumn) {
		comparisonColumn.set(comparisonColumnOptions[0]);
	}

	$: sortedModels = $models.sort((a, b) => a.localeCompare(b));
	$: excludeModels = sortedModels.filter((m) => m !== $model);
	$: sortedMetrics = $metrics.sort((a, b) => a.name.localeCompare(b.name));
</script>

<div class="sticky bg-yellowish-light -top-5 flex items-center pb-2.5 z-10 pt-1">
	{#if $model !== undefined && $models.length > 0}
		<div class="mr-2.5 flex flex-col w-1/2">
			<span class="my-1 text-grey-dark w-fit">
				{$page.url.href.includes('compare') ? 'System A' : 'System'}
			</span>
			<select
				class="w-full h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$model}
			>
				{#each sortedModels as mod}
					<option class="p-1" value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if !$page.url.href.includes('compare') && $metrics.length > 0 && $metric !== undefined}
		<div class="flex flex-col w-1/2">
			<span class="my-1 text-grey-dark">Metric</span>
			<select
				class="w-full h-9 border border-grey-light rounded text-sm text-grey"
				name="metric-select"
				required
				bind:value={$metric}
			>
				{#each sortedMetrics as met}
					<option value={met}>{met.name}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if $page.url.href.includes('compare')}
		<div class="flex flex-col w-1/2">
			<span class="my-1 text-grey-dark">System B</span>
			<select
				class="w-full h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$comparisonModel}
			>
				{#each excludeModels as mod}
					<option value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
</div>

{#if $page.url.href.includes('compare') && comparisonColumnOptions.length > 0}
	<div class="mt-3 mb-3">
		<h4 class="mb-1">Comparison Feature</h4>
		<select
			class="w-full h-9 border border-grey-light rounded text-sm text-grey"
			bind:value={$comparisonColumn}
		>
			{#each comparisonColumnOptions as col (col.id)}
				<option value={col}>{col.name}</option>
			{/each}
		</select>
	</div>
{/if}

{#if $page.url.href.includes('compare') && $metric !== undefined && $metrics.length > 0}
	<div class="flex flex-col w-full mt-3 mb-3">
		<span class="my-1 text-grey-dark">Metric</span>
		<select
			class="w-full h-9 border border-grey-light rounded text-sm text-grey"
			bind:value={$metric}
		>
			{#each sortedMetrics as met}
				<option value={met}>{met.name}</option>
			{/each}
		</select>
	</div>
{/if}
