<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ListView from '$lib/components/instances/ListView.svelte';
	import ProjectHomeElementHeader from '$lib/components/project/ProjectHomeElementHeader.svelte';
	import { metrics, model, models, project } from '$lib/stores';
	import { chartMap } from '$lib/util/charts.js';
	import Button from '@smui/button';

	export let data;

	$: sortedModels = $models.sort((a, b) => a.localeCompare(b));

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}
</script>

<div class="flex min-h-0 w-full min-w-0 gap-4 bg-yellowish p-4">
	<div class="flex h-full min-h-0 w-[600px] flex-col gap-4">
		{#if data.charts.length > 0 && data.charts[0] && data.charts[1]}
			{@const overviewChart = data.charts[1]}
			{@const overviewTable = data.charts[0]}
			<ProjectHomeElementHeader>
				<svelte:component
					this={chartMap[overviewChart.type]}
					chart={overviewChart}
					data={JSON.parse(overviewChart.data ?? '{}')}
					width={500}
					height={400}
				/>
			</ProjectHomeElementHeader>
			<ProjectHomeElementHeader>
				<svelte:component
					this={chartMap[overviewTable.type]}
					chart={overviewTable}
					data={JSON.parse(overviewTable.data ?? '{}')}
					width={900}
				/>
			</ProjectHomeElementHeader>
		{/if}
	</div>
	<ProjectHomeElementHeader>
		<div class="flex min-h-0 w-full min-w-0 items-center">
			<p class="mr-2 font-semibold text-grey-dark">model:</p>
			<select
				class="mr-2 h-9 rounded border border-grey-light text-sm text-grey"
				bind:value={$model}
			>
				{#each sortedModels as mod}
					<option class="p-1" value={mod}>{mod}</option>
				{/each}
			</select>
			<Button
				on:click={() =>
					goto(`/project/${$project.uuid}/${encodeURIComponent($project.name)}/explore`)}
				class="ml-auto">Explore</Button
			>
		</div>
		<div class="flex h-full min-h-0 flex-col">
			<ListView />
		</div>
	</ProjectHomeElementHeader>
</div>
