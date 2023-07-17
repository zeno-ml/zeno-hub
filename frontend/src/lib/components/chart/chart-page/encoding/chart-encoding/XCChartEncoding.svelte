<script lang="ts">
	import { SlicesOrModels, type Chart, type XCParameters } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import MetricsEncodingDropdown from './encoding-components/MetricsEncodingDropdown.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as XCParameters;

	enum Dimensions {
		x,
		color
	}

	function refreshParams(e, currentParam: Dimensions) {
		let label = e.detail.label;
		let paramExcluMap = { slices: SlicesOrModels.MODELS, models: SlicesOrModels.SLICES };

		if (currentParam === Dimensions.x) {
			parameters.xChannel = e.detail.value;
			parameters.colorChannel = paramExcluMap[label];
		}
		if (currentParam === Dimensions.color) {
			parameters.colorChannel = e.detail.value;
			parameters.xChannel = paramExcluMap[label];
		}

		chart = { ...chart, parameters: { ...parameters } };
	}

	function selected(e: CustomEvent<number[] | string[]>, channel: Dimensions) {
		const channelType = channel === Dimensions.x ? parameters.xChannel : parameters.colorChannel;
		if (channelType === SlicesOrModels.SLICES) {
			const slices = e.detail as number[];
			chart = { ...chart, parameters: { ...parameters, slices: slices } };
		} else {
			const models = e.detail as string[];
			chart = { ...chart, parameters: { ...parameters, models: models } };
		}
	}

	function ySelected(e: CustomEvent<number>) {
		chart = { ...chart, parameters: { ...parameters, metric: e.detail } };
	}
</script>

<div class="encoding-section">
	<div class="parameters">
		<h4>x</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.xChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'models', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.xChannel) {
					refreshParams(e, Dimensions.x);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.xChannel].multi}
		on:selected={(e) => selected(e, Dimensions.x)}
		currentValues={parameters.xChannel === SlicesOrModels.SLICES
			? parameters.slices
			: parameters.models}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>y</h4>
		<svelte:component
			this={MetricsEncodingDropdown}
			on:selected={ySelected}
			metric={parameters.metric}
		/>
	</div>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>color</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.colorChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'models', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.colorChannel) {
					refreshParams(e, Dimensions.color);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.colorChannel].multi}
		on:selected={(e) => selected(e, Dimensions.color)}
		currentValues={parameters.colorChannel === SlicesOrModels.SLICES
			? parameters.slices
			: parameters.models}
	/>
</div>

<style>
	.encoding-section {
		margin-bottom: 15px;
	}
	.parameters {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		padding: 10px;
	}
	.parameters h4 {
		margin: 5px;
	}
</style>
