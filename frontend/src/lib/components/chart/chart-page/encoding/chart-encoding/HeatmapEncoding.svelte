<script lang="ts">
	import { models, slices } from '$lib/stores';
	import { SlicesOrModels, type Chart, type HeatmapParameters } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { EncodingMap } from '../encodingUtil';
	import EncodingSection from './EncodingSection.svelte';
	import MetricsEncodingDropdown from './encoding-components/MetricsEncodingDropdown.svelte';
	import ModelsEncodingDropdown from './encoding-components/ModelsEncodingDropdown.svelte';

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

	function selectModel(e: CustomEvent) {
		chart = { ...chart, parameters: { ...parameters, model: e.detail.value } };
	}

	function fixedSelected(e: CustomEvent<number>) {
		chart = { ...chart, parameters: { ...parameters, metric: e.detail } };
	}
</script>

<EncodingSection title="X">
	<svelte:fragment slot="parameters">
		<Svelecte
			value={parameters.xChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshX}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.xChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.x)}
		numberValues={parameters.xChannel === SlicesOrModels.SLICES ? numberValues : []}
		stringValues={parameters.xChannel === SlicesOrModels.MODELS ? stringValues : []}
	/>
</EncodingSection>
<EncodingSection title="Y">
	<svelte:fragment slot="parameters">
		<Svelecte
			value={parameters.yChannel}
			options={[
				{ label: 'slices', value: SlicesOrModels.SLICES },
				{ label: 'systems', value: SlicesOrModels.MODELS }
			]}
			searchable={false}
			on:change={refreshY}
		/>
	</svelte:fragment>
	<svelte:component
		this={EncodingMap[parameters.yChannel].multi}
		slot="component"
		on:selected={(e) => selected(e, Dimensions.y)}
		numberValues={parameters.yChannel === SlicesOrModels.SLICES ? numberValues : []}
		stringValues={parameters.yChannel === SlicesOrModels.MODELS ? stringValues : []}
	/>
</EncodingSection>
<EncodingSection title="System">
	<svelte:fragment slot="parameters">
		<ModelsEncodingDropdown stringValue={parameters.model} on:selected={selectModel} />
	</svelte:fragment>
</EncodingSection>
<EncodingSection title="Color">
	<svelte:fragment slot="parameters">
		<MetricsEncodingDropdown
			on:selected={fixedSelected}
			numberValue={parameters.metric}
			container={false}
		/>
	</svelte:fragment>
</EncodingSection>
