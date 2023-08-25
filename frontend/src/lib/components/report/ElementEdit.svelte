<script lang="ts">
	import { ReportElementType, type ReportElement } from '$lib/zenoapi';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';

	export let element: ReportElement;

	const chartOptions: { id: number; name: string }[] = [];
</script>

<div>
	<Svelecte
		value={element.type === ReportElementType.CHART ? 'Chart' : 'Text'}
		on:change={(e) => {
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
		}}
		style="padding-bottom: 20px;"
		searchable={false}
		valueField="label"
		options={['Chart', 'Text']}
	/>
	{#if element.type === ReportElementType.CHART}
		<div class="ml-8">
			<Svelecte searchable={false} bind:value={element.chartId} options={chartOptions} />
		</div>
	{:else if element.type === ReportElementType.TEXT}
		<div class="ml-8">
			<Textfield textarea label="Text" bind:value={element.data} style="width: 100%;" />
		</div>
	{/if}
</div>
