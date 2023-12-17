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
	import EncodingSection from './EncodingSection.svelte';
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
		let label = e.detail.label as 'systems' | 'slices';
		let paramExcluMap = { slices: SlicesOrModels.MODELS, systems: SlicesOrModels.SLICES };

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

<EncodingSection title="Metric">
	<div class="flex items-center" slot="parameters">
		<span>fixed</span>
		<Checkbox
			checked={fixedDimension === 'metric'}
			on:click={() =>
				(chart = { ...chart, parameters: { ...parameters, fixedDimension: 'metric' } })}
		/>
	</div>
	<svelte:fragment slot="component">
		{#if fixedDimension === 'metric'}
			<MetricsEncodingDropdown on:selected={fixedSelected} numberValue={parameters.metrics[0]} />
		{:else}
			<MetricsEncodingMultiChoice
				on:selected={(e) => selected(e, Dimensions.metric)}
				numberValues={parameters.metrics}
			/>
		{/if}
	</svelte:fragment>
</EncodingSection>
<EncodingSection title="System">
	<div class="flex items-center" slot="parameters">
		<span>fixed</span>
		<Checkbox
			checked={fixedDimension === 'y'}
			on:click={() => (chart = { ...chart, parameters: { ...parameters, fixedDimension: 'y' } })}
		/>
	</div>
	<svelte:fragment slot="component">
		<Svelecte
			value={parameters.yChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshY}
		/>
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
	</svelte:fragment>
</EncodingSection>
<EncodingSection title="Color">
	<svelte:fragment slot="parameters">
		<Svelecte
			value={parameters.colorChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshColor}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.colorChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.color)}
		numberValues={parameters.colorChannel === SlicesOrModels.SLICES ? parameters.slices : []}
		stringValues={parameters.colorChannel === SlicesOrModels.MODELS ? parameters.models : []}
	/>
</EncodingSection>
