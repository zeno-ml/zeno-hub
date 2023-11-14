<script lang="ts">
	import { models } from '$lib/stores';
	import { svelecteRenderer } from '$lib/util/util';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';

	export let stringValue: string;

	const dispatch = createEventDispatcher<{
		selected: string;
	}>();

	let options: { value: string; label: string }[] = [];
	let value = stringValue;

	// initial options & values
	$models.forEach((m) => {
		options.push({ value: m, label: m });
	});

	function valueSelected(e: CustomEvent) {
		if (e.detail.value !== stringValue) {
			dispatch('selected', e.detail);
		}
	}
</script>

<Svelecte
	style="width: 280px; flex:none;"
	bind:value
	{options}
	on:change={valueSelected}
	renderer={svelecteRenderer}
/>
