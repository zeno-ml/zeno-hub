<script lang="ts">
	import type { Chart, ChartConfig } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Textfield from '@smui/textfield';
	import HomeButton from './HomeButton.svelte';
	import SettingsButton from './SettingsButton.svelte';

	export let isChartEdit: boolean;
	export let chart: Chart;
	export let chartConfig: ChartConfig;

	let title = chart.name;

	$: updateChartTitle(title);

	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};

	function updateChartTitle(title: string) {
		chart = { ...chart, name: title };
	}
</script>

<div class="mb-5 mt-5 flex flex-col">
	<div class="mb-5 flex items-center align-middle">
		<HomeButton />
		<Button
			class="ml-3"
			variant="raised"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => (isChartEdit = !isChartEdit)}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
		<SettingsButton bind:chartConfig {chart}></SettingsButton>
	</div>
	<div>
		<Textfield variant="outlined" label="Chart Name" bind:value={title} />
	</div>
</div>
