<script lang="ts">
	import { goto } from '$app/navigation';
	import ChartHomeBlock from '$lib/components/chart/ChartHomeBlock.svelte';
	import { charts, project } from '$lib/stores';
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import Button from '@smui/button/src/Button.svelte';
	import { Icon } from '@smui/icon-button';

	export let data;

	$: charts.set(data.charts);
</script>

<div class="flex flex-col w-full p-6">
	<div class="flex align-center">
		<h3 class="text-xl">Charts</h3>
		{#if $project.editor}
			<Button
				class="ml-auto"
				on:click={() => {
					ZenoService.addChart(
						$project.uuid,
						chartDefaults('New Chart', 0, $project.uuid, ChartType.BAR)
					).then((res) => {
						goto(`/project/${$project.ownerName}/${$project.name}/chart/${res}?edit=true`);
					});
				}}
			>
				<Icon class="mr-2" width="24px" height="24px" tag="svg" viewBox="0 0 24 24">
					<path d={mdiPlus} />
				</Icon>
				New Chart
			</Button>
		{/if}
	</div>
	<div class="w-full mb-4 h-1 bg-grey-light rounded-full" />
	<div class="flex flex-wrap overflow-y-auto">
		{#each $charts.sort((a, b) => a.id - b.id) as chart}
			<ChartHomeBlock {chart} />
		{/each}
	</div>
</div>
