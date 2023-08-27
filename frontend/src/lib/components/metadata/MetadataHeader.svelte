<script lang="ts">
	import { page } from '$app/stores';
	import { comparisonModel, metric, metrics, model, models } from '$lib/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		if ($model === undefined && $models.length > 0) {
			model.set($models[0]);
		}
		if ($metric === undefined && $metrics.length > 0) {
			metric.set($metrics[0]);
		}
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
	$: if (
		$metric === undefined ||
		(-1 ===
			$metrics.findIndex(
				(currentMetric) => currentMetric.id === ($metric === undefined ? -1 : $metric.id)
			) &&
			$metrics.length > 0)
	) {
		$metric = $metrics[0];
	}
</script>

<div class="sticky bg-yellowish-light -top-5 flex items-center pb-2.5 z-10 pt-1 w-96">
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
	{#if !$page.url.href.includes('compare') && $metric !== undefined}
		<div class="flex flex-col w-1/2">
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
{#if $page.url.href.includes('compare') && $metric !== undefined}
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
