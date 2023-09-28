<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type Chart,
		type TableParameters
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import EncodingSection from './EncodingSection.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as TableParameters;

	enum Dimensions {
		x,
		y,
		fixed
	}

	function refreshParams(e: CustomEvent, currentParam: Dimensions) {
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

	function xChanged(e: CustomEvent) {
		if (e.detail.value !== parameters.xChannel) {
			refreshParams(e, Dimensions.x);
		}
	}

	function yChanged(e: CustomEvent) {
		if (e.detail.value !== parameters.yChannel) {
			refreshParams(e, Dimensions.y);
		}
	}

	function fixedChanged(e: CustomEvent) {
		if (e.detail.value !== parameters.fixedChannel) {
			refreshParams(e, Dimensions.fixed);
		}
	}
</script>

<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>x</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.xChannel}
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'systems', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={xChanged}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.xChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.x)}
		numberValues={parameters.xChannel === SlicesMetricsOrModels.SLICES
			? parameters.slices
			: parameters.fixedChannel === SlicesMetricsOrModels.METRICS
			? parameters.metrics
			: []}
		stringValues={parameters.xChannel === SlicesMetricsOrModels.MODELS ? parameters.models : []}
	/>
</EncodingSection>
<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>y</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.yChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={yChanged}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.yChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.y)}
		numberValues={parameters.yChannel === SlicesOrModels.SLICES ? parameters.slices : []}
		stringValues={parameters.yChannel === SlicesOrModels.MODELS ? parameters.models : []}
	/>
</EncodingSection>
<EncodingSection>
	<svelte:fragment slot="parameters">
		<h4>fixed</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none"
			value={parameters.fixedChannel}
			slot="component"
			options={[
				{ label: 'slices', value: SlicesMetricsOrModels.SLICES },
				{ label: 'systems', value: SlicesMetricsOrModels.MODELS },
				{ label: 'metrics', value: SlicesMetricsOrModels.METRICS }
			]}
			searchable={false}
			on:change={fixedChanged}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.fixedChannel].fixed}
		on:selected={fixedSelected}
		slot="component"
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
