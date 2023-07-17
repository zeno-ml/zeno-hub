<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type Chart,
		type RadarParameters
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';

	export let chart: Chart;

	$: parameters = chart.parameters as RadarParameters;

	enum Dimensions {
		axis,
		layer,
		fixed
	}

	function refreshParams(e, currentParam: Dimensions) {
		if (currentParam === Dimensions.axis) {
			parameters.axisChannel = e.detail.value;
			if (e.detail.value === SlicesMetricsOrModels.METRICS) {
				parameters.fixedChannel =
					parameters.layerChannel === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.fixedChannel = SlicesMetricsOrModels.METRICS;
				parameters.layerChannel =
					e.detail.value === SlicesMetricsOrModels.MODELS
						? SlicesOrModels.SLICES
						: SlicesOrModels.MODELS;
			}
		} else if (currentParam === Dimensions.layer) {
			parameters.layerChannel = e.detail.value;
			if (parameters.axisChannel === SlicesMetricsOrModels.METRICS) {
				parameters.fixedChannel =
					e.detail.value === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.axisChannel =
					e.detail.value === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			}
		} else if (currentParam === Dimensions.fixed) {
			parameters.fixedChannel = e.detail.value;
			if (e.detail.value === SlicesMetricsOrModels.METRICS) {
				parameters.axisChannel =
					parameters.layerChannel === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.axisChannel = SlicesMetricsOrModels.METRICS;
				parameters.layerChannel =
					e.detail.value === SlicesMetricsOrModels.MODELS
						? SlicesOrModels.SLICES
						: SlicesOrModels.MODELS;
			}
		}

		chart = { ...chart, parameters: { ...parameters } };
	}

	function selected(e: CustomEvent<number[] | string[]>, channel: Dimensions) {
		const channelType =
			channel === Dimensions.axis ? parameters.axisChannel : parameters.layerChannel;
		switch (channelType) {
			case SlicesMetricsOrModels.SLICES:
				chart = { ...chart, parameters: { ...parameters, slices: e.detail as number[] } };
				break;
			case SlicesMetricsOrModels.MODELS:
				chart = { ...chart, parameters: { ...parameters, models: e.detail as string[] } };
				break;
			case SlicesMetricsOrModels.METRICS:
				chart = { ...chart, parameters: { ...parameters, metrics: e.detail as number[] } };
				break;
		}
	}

	function fixedSelected(e: CustomEvent<number | string>) {
		switch (parameters.fixedChannel) {
			case SlicesMetricsOrModels.METRICS:
				chart = { ...chart, parameters: { ...parameters, metrics: [e.detail as number] } };
				break;
			case SlicesMetricsOrModels.SLICES:
				chart = { ...chart, parameters: { ...parameters, slices: [e.detail as number] } };
				break;
			case SlicesMetricsOrModels.MODELS:
				chart = { ...chart, parameters: { ...parameters, models: [e.detail as string] } };
				break;
		}
	}
</script>

<div class="encoding-section">
	<div class="parameters">
		<h4>axis</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.axisChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'models', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.axisChannel) {
					refreshParams(e, Dimensions.axis);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.axisChannel].multi}
		on:selected={(e) => selected(e, Dimensions.axis)}
		currentValues={parameters.axisChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices
			: parameters.axisChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics
			: parameters.models}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>color</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.layerChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'models', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.layerChannel) {
					refreshParams(e, Dimensions.layer);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.layerChannel].multi}
		on:selected={(e) => selected(e, Dimensions.x)}
		currentValues={parameters.layerChannel === SlicesOrModels.SLICES
			? parameters.slices
			: parameters.models}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>value</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.fixedChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'models', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={(e) => {
				if (e.detail.value !== parameters.fixedChannel) {
					refreshParams(e, Dimensions.fixed);
				}
			}}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.fixedChannel].fixed}
		on:selected={(e) => fixedSelected(e)}
		currentValue={parameters.fixedChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices[0]
			: parameters.fixedChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics[0]
			: parameters.models[0]}
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
