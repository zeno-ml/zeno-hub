<script lang="ts">
	import {
		SlicesOrModels,
		type Chart,
		type BeeswarmParameters,
		SlicesMetricsOrModels
	} from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import MetricsEncodingDropdown from '../MetricsEncodingDropdown.svelte';
	import MetricsEncodingMultiChoice from '../MetricsEncodingMultiChoice.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as BeeswarmParameters;

	enum Dimensions {
		y,
		color,
		metric
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
		const channelType =
			channel === Dimensions.x
				? parameters.xChannel
				: Dimensions.metric
				? SlicesMetricsOrModels.METRICS
				: parameters.colorChannel;
		if (channelType === SlicesOrModels.SLICES) {
			const slices = e.detail as number[];
			chart = { ...chart, parameters: { ...parameters, slices: slices } };
		} else if (channelType === SlicesMetricsOrModels.METRICS) {
			const metrics = e.detail as number[];
			chart = { ...chart, parameters: { ...parameters, metrics: metrics } };
		} else {
			const models = e.detail as string[];
			chart = { ...chart, parameters: { ...parameters, models: models } };
		}
	}

	function fixedSelected(e: CustomEvent<number | string>) {
		if (parameters.fixedDimension === 'metric') {
			chart = { ...chart, parameters: { ...parameters, metrics: [e.detail] } };
		} else {
			if (parameters.yChannel === SlicesOrModels.MODELS) {
				chart = { ...chart, parameters: { ...parameters, models: [e.detail] } };
			} else {
				chart = { ...chart, parameters: { ...parameters, slices: [e.detail] } };
			}
		}
	}
</script>

<div class="encoding-section">
	<div class="parameters">
		<h4>metric</h4>
		<Checkbox
			checked={parameters.fixedDimension === 'metric'}
			onclick={() =>
				(chart = { ...chart, parameters: { ...parameters, checkedDimension: 'metric' } })}
		/>
	</div>
	{#if parameters.fixedDimension === 'metric'}
		<svelte:component
			this={MetricsEncodingDropdown}
			on:selected={(e) => fixedSelected(e)}
			currentValues={parameters.metrics[0]}
		/>
	{:else}
		<svelte:component
			this={MetricsEncodingMultiChoice}
			on:selected={(e) => selected(e, Dimensions.metric)}
			currentValues={parameters.metrics}
		/>
	{/if}
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
		<Checkbox
			checked={parameters.fixedDimension === 'y'}
			onclick={() => (chart = { ...chart, parameters: { ...parameters, checkedDimension: 'y' } })}
		/>
	</div>
	{#if parameters.fixedDimension === 'y'}
		<svelte:component
			this={EncodingMap[parameters.yChannel].fixed}
			on:selected={(e) => fixedSelected(e)}
			currentValues={parameters.yChannel === SlicesOrModels.MODELS
				? parameters.models[0]
				: parameters.slices[0]}
		/>
	{:else}
		<svelte:component
			this={EncodingMap[parameters.yChannel].multi}
			on:selected={(e) => fixedSelected(e, Dimensions.y)}
			currentValues={parameters.yChannel === SlicesOrModels.MODELS
				? parameters.models
				: parameters.slices}
		/>
	{/if}
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
		on:selected={(e) => fixedSelected(e, Dimensions.color)}
		currentValues={parameters.colorChannel === SlicesOrModels.MODELS
			? parameters.models
			: parameters.slices}
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
