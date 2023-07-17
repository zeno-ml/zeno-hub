<script lang="ts">
	import { models, slices } from '$lib/stores';
	import { SlicesOrModels, type Chart, type HeatmapParameters } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import MetricsEncodingDropdown from './encoding-components/MetricsEncodingDropdown.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as HeatmapParameters;

	enum Dimensions {
		x,
		y
	}

	function refreshParams(e, currentParam: Dimensions) {
		const settingModels = e.detail.value === SlicesOrModels.MODELS;
		if (currentParam === Dimensions.x) {
			parameters.xChannel = e.detail.value;
			parameters.xValues = settingModels
				? $models.slice(0, 2)
				: $slices.slice(0, 2).map((slice) => slice.id);
			if (settingModels) {
				parameters.yChannel = SlicesOrModels.SLICES;
				parameters.yValues = $slices.slice(0, 2).map((slice) => slice.id);
			}
		}
		if (currentParam === Dimensions.y) {
			parameters.yChannel = e.detail.value;
			parameters.yValues = settingModels
				? $models.slice(0, 2)
				: $slices.slice(0, 2).map((slice) => slice.id);
			if (settingModels) {
				parameters.xChannel = SlicesOrModels.SLICES;
				parameters.xValues = $slices.slice(0, 2).map((slice) => slice.id);
			}
		}

		chart = { ...chart, parameters: { ...parameters } };
	}

	function selected(e: CustomEvent<number[] | string[]>, channel: Dimensions) {
		if (channel === Dimensions.x) {
			chart = { ...chart, parameters: { ...parameters, xValues: e.detail } };
		} else {
			chart = { ...chart, parameters: { ...parameters, yValues: e.detail } };
		}
	}

	function fixedSelected(e: CustomEvent<number>) {
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
		currentValues={parameters.xValues}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>y</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.yChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'models', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.yChannel) {
					refreshParams(e, Dimensions.y);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.yChannel].multi}
		on:selected={(e) => selected(e, Dimensions.y)}
		currentValues={parameters.yValues}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>color</h4>
		<MetricsEncodingDropdown on:selected={fixedSelected} currentValue={parameters.metric} />
	</div>
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
