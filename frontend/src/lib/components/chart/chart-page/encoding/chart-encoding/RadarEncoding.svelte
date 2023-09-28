<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type Chart,
		type RadarParameters
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import EncodingSection from './EncodingSection.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as RadarParameters;

	enum Dimensions {
		axis,
		layer,
		fixed
	}

	function refreshParams(e: CustomEvent, currentParam: Dimensions) {
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

	function refreshAxisParams(e: CustomEvent) {
		refreshParams(e, Dimensions.axis);
	}

	function refreshLayerParams(e: CustomEvent) {
		refreshParams(e, Dimensions.layer);
	}

	function refreshFixedParams(e: CustomEvent) {
		refreshParams(e, Dimensions.fixed);
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

	function fixedSelected(e: CustomEvent) {
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

<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>axis</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.axisChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'systems', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={refreshAxisParams}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.axisChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.axis)}
		numberValues={parameters.axisChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices
			: parameters.axisChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics
			: []}
		stringValues={parameters.axisChannel === SlicesMetricsOrModels.MODELS ? parameters.models : []}
	/>
</EncodingSection>
<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>color</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.layerChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshLayerParams}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.layerChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.layer)}
		numberValues={parameters.layerChannel === SlicesOrModels.SLICES ? parameters.slices : []}
		stringValues={parameters.layerChannel === SlicesOrModels.MODELS ? parameters.models : []}
	/>
</EncodingSection>
<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>value</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.fixedChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'systems', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={refreshFixedParams}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.fixedChannel].fixed}
		slot="component"
		on:selected={fixedSelected}
		numberValue={parameters.fixedChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices[0]
			: parameters.fixedChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics[0]
			: 0}
		stringValue={parameters.fixedChannel === SlicesMetricsOrModels.MODELS
			? parameters.models[0]
			: ''}
	/>
</EncodingSection>
