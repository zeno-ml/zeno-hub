<script lang="ts">
	import { models, slices } from '$lib/stores';
	import { SlicesOrModels, type Chart, type HeatmapParameters } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import MetricsEncodingDropdown from './encoding-components/MetricsEncodingDropdown.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as HeatmapParameters;
	$: numberValues =
		parameters.xChannel === SlicesOrModels.SLICES
			? (parameters.xValues as number[])
			: (parameters.yValues as number[]);
	$: stringValues =
		parameters.xChannel === SlicesOrModels.MODELS
			? (parameters.xValues as string[])
			: (parameters.yValues as string[]);

	enum Dimensions {
		x,
		y
	}

	function refreshParams(e: CustomEvent, currentParam: Dimensions) {
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

	function refreshX(e: CustomEvent) {
		refreshParams(e, Dimensions.x);
	}

	function refreshY(e: CustomEvent) {
		refreshParams(e, Dimensions.y);
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
			on:change={refreshX}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.xChannel].multi}
		on:selected={(e) => selected(e, Dimensions.x)}
		numberValues={parameters.xChannel === SlicesOrModels.SLICES ? numberValues : []}
		stringValues={parameters.xChannel === SlicesOrModels.MODELS ? stringValues : []}
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
			on:change={refreshY}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.yChannel].multi}
		on:selected={(e) => selected(e, Dimensions.y)}
		numberValues={parameters.yChannel === SlicesOrModels.SLICES ? numberValues : []}
		stringValues={parameters.yChannel === SlicesOrModels.MODELS ? stringValues : []}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>color</h4>
		<MetricsEncodingDropdown on:selected={fixedSelected} numberValue={parameters.metric} />
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
