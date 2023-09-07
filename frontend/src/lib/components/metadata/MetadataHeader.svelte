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
	import type { ZenoColumn } from '$lib/zenoapi';
	import { onMount } from 'svelte';

	let comparisonColumnOptions: ZenoColumn[] = [];

	onMount(() => {
		comparisonColumnOptions = $columns.filter((c) => c.model === $model);
		comparisonColumn.set(comparisonColumnOptions[0]);
	});

	$: exludeModels = $models.filter((m) => m !== $model);
	$: if ($model === undefined || (!$models.includes($model) && $models.length > 0)) {
		$model = $models[0];
	}
	$: if (
		$comparisonModel === undefined ||
		(!$models.includes($comparisonModel) && $models.length > 1)
	) {
		$model = $models[1];
	}
</script>

<div class="sticky bg-yellowish-light -top-5 flex items-center pb-2.5 z-10 pt-1">
	{#if $model !== undefined && $models.length > 0}
		<div class="mr-2.5 flex flex-col w-1/2">
			<span class="my-1 text-grey-dark w-fit">
				{$page.url.href.includes('compare') ? 'Model A' : 'Model'}
			</span>
			<select
				class="w-full h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$model}
			>
				{#each $models as mod}
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
				{#each $metrics as met}
					<option value={met}>{met.name}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if $page.url.href.includes('compare')}
		<div class="flex flex-col w-1/2">
			<span class="my-1 text-grey-dark">Model B</span>
			<select
				class="w-full h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$comparisonModel}
			>
				{#each exludeModels as mod}
					<option value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
</div>
{#if $page.url.href.includes('compare') && $metric !== undefined && $metrics.length > 0}
	<div class="flex flex-col w-full">
		<span class="my-1 text-grey-dark">Metric</span>
		<select
			class="w-full h-9 border border-grey-light rounded text-sm text-grey"
			bind:value={$metric}
		>
			{#each $metrics as met}
				<option value={met}>{met.name}</option>
			{/each}
		</select>
	</div>
{/if}

{#if $page.url.href.includes('compare')}
	<div class="mt-3 mb-3">
		<h4 class="mb-1">Comparison Feature</h4>
		<select
			class="w-full h-9 border border-grey-light rounded text-sm text-grey"
			bind:value={$comparisonColumn}
		>
			{#each comparisonColumnOptions as col}
				<option value={col}>{col.name}</option>
			{/each}
		</select>
	</div>
{/if}
