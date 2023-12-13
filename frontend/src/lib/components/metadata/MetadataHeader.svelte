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
	import Select from '../ui/Select.svelte';

	let comparisonColumnOptions = $columns.filter((c) => c.model === $model);
	if (!$comparisonColumn) {
		comparisonColumn.set(comparisonColumnOptions[0]);
	}

	$: sortedModels = $models.sort((a, b) => a.localeCompare(b));
	$: excludeModels = sortedModels.filter((m) => m !== $model);
	$: sortedMetrics = $metrics.sort((a, b) => a.name.localeCompare(b.name));
</script>

<div class="sticky -top-2 z-10 flex items-center bg-yellowish-light py-1">
	{#if $model !== undefined && $models.length > 0}
		<div class="mr-2.5 flex w-1/2 flex-col">
			<span class="my-1 w-fit text-grey-dark">
				{$page.url.href.includes('compare') ? 'System A' : 'System'}
			</span>
			<Select
				bind:value={$model}
				options={sortedModels.map((model) => {
					return { value: model, label: model };
				})}
			/>
		</div>
	{/if}
	{#if !$page.url.href.includes('compare') && $metrics.length > 0 && $metric !== undefined}
		<div class="flex w-1/2 flex-col">
			<span class="my-1 text-grey-dark">Metric</span>
			<Select
				bind:value={$metric}
				options={sortedMetrics.map((metric) => {
					return { value: metric, label: metric.name };
				})}
			/>
		</div>
	{/if}
	{#if $page.url.href.includes('compare')}
		<div class="flex w-1/2 flex-col">
			<span class="my-1 text-grey-dark">System B</span>
			<Select
				bind:value={$comparisonModel}
				options={excludeModels.map((model) => {
					return { value: model, label: model };
				})}
			/>
		</div>
	{/if}
</div>

{#if $page.url.href.includes('compare') && comparisonColumnOptions.length > 0}
	<div class="my-3">
		<h4 class="mb-1">Comparison Feature</h4>
		<Select
			bind:value={$comparisonColumn}
			options={comparisonColumnOptions.map((col) => {
				return { value: col, label: col.name };
			})}
		/>
	</div>
{/if}

{#if $page.url.href.includes('compare') && $metric !== undefined && $metrics.length > 0}
	<div class="my-3 flex w-full flex-col">
		<span class="my-1 text-grey-dark">Metric</span>
		<Select
			bind:value={$metric}
			options={sortedMetrics.map((metric) => {
				return { value: metric, label: metric.name };
			})}
		/>
	</div>
{/if}
