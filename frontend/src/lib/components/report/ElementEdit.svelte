<script lang="ts">
	import { ReportElementType, type Chart, type ReportElement } from '$lib/zenoapi';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';

	export let element: ReportElement;
	export let chartOptions: Promise<Chart[]>;

	function setDefaults(e: CustomEvent) {
		if (e.detail.label === 'Chart') {
			element = {
				id: element.id,
				data: null,
				chartId: null,
				type: ReportElementType.CHART,
				position: element.position
			};
		} else {
			element = {
				id: element.id,
				data: '',
				chartId: null,
				type: ReportElementType.TEXT,
				position: element.position
			};
		}
	}
</script>

<div">
	<Svelecte
		value={element.type === ReportElementType.CHART ? 'Chart' : 'Text'}
		on:change={setDefaults}
		style="padding-bottom: 20px;"
		searchable={false}
		valueField="label"
		options={['Chart', 'Text']}
	/>
	{#if element.type === ReportElementType.CHART}
		{#await chartOptions then options}
			<div class="ml-8">
				<Svelecte searchable={false} bind:value={element.chartId} {options} />
			</div>
		{/await}
	{:else if element.type === ReportElementType.TEXT}
		<div class="ml-8">
			<Textfield textarea label="Text" bind:value={element.data} style="width: 100%;" />
		</div>
	{/if}
</div>
