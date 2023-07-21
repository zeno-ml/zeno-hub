<script lang="ts">
	import {
		SlicesMetricsOrModels,
		SlicesOrModels,
		type BeeswarmParameters,
		type Chart
	} from '$lib/zenoapi';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import MetricsEncodingDropdown from './encoding-components/MetricsEncodingDropdown.svelte';
	import MetricsEncodingMultiChoice from './encoding-components/MetricsEncodingMultiChoice.svelte';

	export let chart: Chart;

	$: parameters = chart.parameters as BeeswarmParameters;
	$: fixedDimension = parameters.fixedDimension;

	enum Dimensions {
		y,
		color,
		metric
	}

	function refreshParams(e: CustomEvent, currentParam: Dimensions) {
		let label = e.detail.label as 'models' | 'slices';
		let paramExcluMap = { slices: SlicesOrModels.MODELS, models: SlicesOrModels.SLICES };

		if (currentParam === Dimensions.y) {
			parameters.yChannel = e.detail.value;
			parameters.colorChannel = paramExcluMap[label];
		}
		if (currentParam === Dimensions.color) {
			parameters.colorChannel = e.detail.value;
			parameters.yChannel = paramExcluMap[label];
		}

		chart = { ...chart, parameters: { ...parameters } };
	}

	function refreshY(e: CustomEvent) {
		refreshParams(e, Dimensions.y);
	}

	function refreshColor(e: CustomEvent) {
		refreshParams(e, Dimensions.color);
	}

	function selected(e: CustomEvent<number[] | string[]>, channel: Dimensions) {
		const channelType =
			channel === Dimensions.y
				? parameters.yChannel
				: channel === Dimensions.metric
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

	function fixedSelected(e: CustomEvent) {
		if (fixedDimension === 'metric') {
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
		<div class="fixed-container">
			<span>fixed</span>
			<Checkbox
				checked={fixedDimension === 'metric'}
				on:click={() =>
					(chart = { ...chart, parameters: { ...parameters, fixedDimension: 'metric' } })}
			/>
		</div>
	</div>
	{#if fixedDimension === 'metric'}
		<MetricsEncodingDropdown on:selected={fixedSelected} numberValue={parameters.metrics[0]} />
	{:else}
		<MetricsEncodingMultiChoice
			on:selected={(e) => selected(e, Dimensions.metric)}
			numberValues={parameters.metrics}
		/>
	{/if}
</div>
<div class="encoding-section">
	<div class="parameters">
		<h4>y</h4>
		<div class="fixed-container">
			<span>fixed</span>
			<Checkbox
				checked={fixedDimension === 'y'}
				on:click={() => (chart = { ...chart, parameters: { ...parameters, fixedDimension: 'y' } })}
			/>
		</div>
	</div>
	<div class="parameters">
		<h4 class="select-label">&nbsp;</h4>
		<Svelecte
			style="width: 280px; height: 30px; flex:none;"
			value={parameters.yChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'models', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshY}
		/>
	</div>
	{#if fixedDimension === 'y'}
		<svelte:component
			this={EncodingMap[parameters.yChannel].fixed}
			on:selected={fixedSelected}
			numberValue={parameters.yChannel === SlicesOrModels.SLICES ? parameters.slices[0] : 0}
			stringValue={parameters.yChannel === SlicesOrModels.MODELS ? parameters.models[0] : ''}
		/>
	{:else}
		<svelte:component
			this={EncodingMap[parameters.yChannel].multi}
			on:selected={(e) => selected(e, Dimensions.y)}
			numberValues={parameters.yChannel === SlicesOrModels.SLICES ? parameters.slices : []}
			stringValues={parameters.yChannel === SlicesOrModels.MODELS ? parameters.models : []}
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
			on:change={refreshColor}
		/>
	</div>
	<svelte:component
		this={EncodingMap[parameters.colorChannel].multi}
		on:selected={(e) => selected(e, Dimensions.color)}
		numberValues={parameters.colorChannel === SlicesOrModels.SLICES ? parameters.slices : []}
		stringValues={parameters.colorChannel === SlicesOrModels.MODELS ? parameters.models : []}
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
	.fixed-container {
		display: flex;
		align-items: center;
	}
	.parameters {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		padding: 10px;
	}
</style>
