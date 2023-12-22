<script lang="ts">
	import { project } from '$lib/stores';
	import type { Chart, ChartConfig } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import HomeButton from './HomeButton.svelte';
	import SettingsButton from './SettingsButton.svelte';

	export let chart: Chart;
	export let isChartEdit: boolean | undefined;
	export let chartConfig: ChartConfig;

	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};
</script>

<div class="ml-5 mt-5 flex cursor-pointer items-center">
	<HomeButton />
	{#if $project.editor}
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
	{/if}
</div>
