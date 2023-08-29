<script lang="ts">
	import type { Chart } from '$lib/zenoapi';
	import Button, { Label } from '@smui/button';
	import Textfield from '@smui/textfield';
	import HomeButton from './HomeButton.svelte';

	export let isChartEdit: boolean;
	export let chart: Chart;

	let title = chart.name;

	$: updateChartTitle(title);

	let blur = function (ev: CustomEvent) {
		ev.target && (ev.target as HTMLElement).blur();
	};

	function updateChartTitle(title: string) {
		chart = { ...chart, name: title };
	}
</script>

<div class="flex flex-col mb-5 mt-5">
	<div class="flex items-center mb-5 align-middle">
		<HomeButton />
		<Button
			class="ml-3"
			variant="outlined"
			on:mouseleave={blur}
			on:focusout={blur}
			on:click={() => (isChartEdit = !isChartEdit)}
		>
			<Label>{isChartEdit ? 'View' : 'Edit'}</Label>
		</Button>
	</div>
	<div>
		<Textfield
			style="width: -webkit-fill-available"
			variant="outlined"
			label="Chart Name"
			bind:value={title}
		/>
	</div>
</div>
