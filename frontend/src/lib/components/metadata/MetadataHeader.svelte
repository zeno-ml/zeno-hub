<script lang="ts">
	import { page } from '$app/stores';
	import { comparisonModel, metric, metrics, model, models } from '$lib/stores';

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

<div id="sticky bg-yellowish-light -top-2.5 flex items-center pb-2.5 pt-1">
	{#if $model !== undefined && $models.length > 1}
		<div style="margin-right: 10px;">
			<div class="my-1 text-grey-dark">
				{$page.url.href.includes('compare') ? 'Model A' : 'Model'}
			</div>
			<select
				class="w-40 h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$model}
			>
				{#each $models as mod}
					<option class="p-1" value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if !$page.url.href.includes('compare') && $metric !== undefined}
		<div>
			<div class="my-1 text-grey-dark">Metric</div>
			<select
				class="w-40 h-9 border border-grey-light rounded text-sm text-grey"
				bind:value={$metric}
			>
				{#each $metrics as met}
					<option value={met}>{met.name}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if $page.url.href.includes('compare')}
		<div>
			<div class="my-1 text-grey-dark">Model B</div>
			<select
				class="w-40 h-9 border border-grey-light rounded text-sm text-grey"
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
	<div>
		<div class="my-1 text-grey-dark">Metric</div>
		<select
			class="w-80 h-9 border border-grey-light rounded text-sm text-grey"
			bind:value={$metric}
		>
			{#each $metrics as met}
				<option value={met}>{met.name}</option>
			{/each}
		</select>
	</div>
{/if}
