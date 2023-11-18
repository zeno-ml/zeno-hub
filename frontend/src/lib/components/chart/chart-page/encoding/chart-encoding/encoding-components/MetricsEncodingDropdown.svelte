<script lang="ts">
	import { metrics } from '$lib/stores';
	import { svelecteRenderer } from '$lib/util/util';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let numberValue: number;
	export let container = true;

	const dispatch = createEventDispatcher<{
		selected: number;
	}>();

	let options: { value: number; label: string }[] = [];
	let value = 0;

	options.push({ value: -1, label: 'slice size' });
	$metrics.forEach((m) => {
		options.push({ value: m.id, label: m.name });
	});
	value = numberValue;

	function valueSelected(e: CustomEvent) {
		if (e.detail.value !== numberValue) {
			dispatch('selected', e.detail.value);
		}
	}
</script>

{#if container}
	<Svelecte bind:value {options} on:change={valueSelected} renderer={svelecteRenderer} />
{:else}
	<Svelecte bind:value {options} on:change={valueSelected} renderer={svelecteRenderer} />
{/if}
