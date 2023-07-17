<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type Chart,
		type TableParameters
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';

	export let chart: Chart;

	$: parameters = chart.parameters as TableParameters;

	enum Dimensions {
		x,
		y,
		fixed
	}

	function refreshParams(e, currentParam: Dimensions) {
		if (currentParam === Dimensions.x) {
			parameters.xChannel = e.detail.value;
			if (e.detail.value === SlicesMetricsOrModels.METRICS) {
				parameters.fixedChannel =
					parameters.yChannel === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.fixedChannel = SlicesMetricsOrModels.METRICS;
				parameters.yChannel =
					e.detail.value === SlicesMetricsOrModels.MODELS
						? SlicesOrModels.SLICES
						: SlicesOrModels.MODELS;
			}
		} else if (currentParam === Dimensions.y) {
			parameters.yChannel = e.detail.value;
			if (parameters.xChannel === SlicesMetricsOrModels.METRICS) {
				parameters.fixedChannel =
					e.detail.value === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.xChannel =
					e.detail.value === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			}
		} else if (currentParam === Dimensions.fixed) {
			parameters.fixedChannel = e.detail.value;
			if (e.detail.value === SlicesMetricsOrModels.METRICS) {
				parameters.xChannel =
					parameters.yChannel === SlicesOrModels.MODELS
						? SlicesMetricsOrModels.SLICES
						: SlicesMetricsOrModels.MODELS;
			} else {
				parameters.xChannel = SlicesMetricsOrModels.METRICS;
				parameters.yChannel =
					e.detail.value === SlicesMetricsOrModels.MODELS
						? SlicesOrModels.SLICES
						: SlicesOrModels.MODELS;
			}
		}

		chart = { ...chart, parameters: { ...parameters } };
	}

	function selected(e: CustomEvent<number[] | string[]>, channel: Dimensions) {
		const channelType = channel === Dimensions.x ? parameters.xChannel : parameters.yChannel;
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
		<h4>x</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.xChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'models', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
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
		currentValues={parameters.xChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices
			: parameters.xChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics
			: parameters.models}
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
		currentValues={parameters.yChannel === SlicesOrModels.SLICES
			? parameters.slices
			: parameters.models}
	/>
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>color</h4>
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
