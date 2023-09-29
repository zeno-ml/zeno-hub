<script lang="ts">
	import { goto } from '$app/navigation';
	import ChartHomeBlock from '$lib/components/chart/ChartHomeBlock.svelte';
	import { charts, project } from '$lib/stores';
	import { chartDefaults } from '$lib/util/charts';
	import { ChartType, ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/icon-button';

	export let data;

	$: charts.set(data.charts);
</script>

<div class="flex flex-col w-full bg-yellowish">
	<div class="flex flex-col bg-white p-6 m-4 shadow rounded">
		<div class="flex align-center mb-7">
			<h3 class="text-xl mr-5">Charts</h3>
			{#if $project.editor}
				<button
					class="border-solid rounded-sm border-grey-light border shadow-sm flex flex-col hover:shadow-md p-1 pr-3 pl-1"
					on:click={() => {
						ZenoService.addChart(
							$project.uuid,
							chartDefaults('New Chart', 0, $project.uuid, ChartType.BAR)
						).then((res) => {
							goto(`/project/${$project.ownerName}/${$project.name}/chart/${res}?edit=true`);
						});
					}}
				>
					<div class="flex items-center">
						<Icon
							class="mr-2"
							style="outline:none;"
							width="24px"
							height="24px"
							tag="svg"
							viewBox="0 0 24 24"
						>
							<path fill="black" d={mdiPlus} />
						</Icon>
						New Chart
					</div>
				</button>
			{/if}
		</div>
		<div class="flex flex-wrap overflow-y-auto">
			{#each $charts.sort((a, b) => a.id - b.id) as chart}
				<ChartHomeBlock {chart} />
			{/each}
		</div>
	</div>
</div>
