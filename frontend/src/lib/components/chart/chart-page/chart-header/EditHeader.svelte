<script lang="ts">
	import type { Chart } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Textfield from '@smui/textfield';
	import { noop } from 'svelte/internal';
	import HomeButton from './HomeButton.svelte';

	export let isChartEdit: boolean;
	export let chart: Chart;
	export let updateChart: () => void = noop;

	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};
</script>

<div class="flex flex-col mb-5">
	<div class="flex items-center justify-between">
		<HomeButton />
		<Button
			style="width: 24px; height: 24px;margin-bottom:3px;background-color:var(--G5)"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => {
				isChartEdit = !isChartEdit;
				updateChart();
			}}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
	</div>
	<div>
		<Textfield
			style="width: -webkit-fill-available"
			variant="outlined"
			bind:value={chart.name}
			label="Chart Name"
		/>
	</div>
</div>
