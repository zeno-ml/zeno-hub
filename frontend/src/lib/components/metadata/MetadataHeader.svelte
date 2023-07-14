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

<div id="selections">
	{#if $model !== undefined && $models.length > 1}
		<div style="margin-right: 10px;">
			<div class="options-header">
				{$page.url.href.includes('compare') ? 'Model A' : 'Model'}
			</div>
			<select bind:value={$model}>
				{#each $models as mod}
					<option value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if !$page.url.href.includes('compare') && $metric !== undefined}
		<div>
			<div class="options-header">Metric</div>
			<select bind:value={$metric}>
				{#each $metrics as met}
					<option value={met}>{met.name}</option>
				{/each}
			</select>
		</div>
	{/if}
	{#if $page.url.href.includes('compare')}
		<div>
			<div class="options-header">Model B</div>
			<select bind:value={$comparisonModel}>
				{#each exludeModels as mod}
					<option value={mod}>{mod}</option>
				{/each}
			</select>
		</div>
	{/if}
</div>
{#if $page.url.href.includes('compare') && $metric !== undefined}
	<div>
		<div class="options-header">Metric</div>
		<select style="width: 345px" bind:value={$metric}>
			{#each $metrics as met}
				<option value={met}>{met.name}</option>
			{/each}
		</select>
	</div>
{/if}

<style>
	select {
		width: 167px;
		height: 35px;
		border: 1px solid var(--G4);
		border-radius: 4px;
		font-size: 14px;
		color: var(--G1);
	}
	option {
		padding: 5px;
	}
	option:checked {
		background-color: var(--G5);
	}
	.options-header {
		margin-top: 5px;
		margin-bottom: 5px;
		color: var(--G2);
	}
	#selections {
		position: sticky;
		background-color: var(--Y2);
		z-index: 3;
		top: -10px;
		display: flex;
		flex-direction: row;
		align-items: center;
		padding-bottom: 10px;
		padding-top: 5px;
	}
	.options-header {
		margin-top: 5px;
		margin-bottom: 5px;
		color: var(--G2);
	}
</style>
