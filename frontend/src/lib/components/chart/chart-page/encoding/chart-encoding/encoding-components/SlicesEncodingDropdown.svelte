<script lang="ts">
	import { slices } from '$lib/stores';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import EncodingContainer from './EncodingContainer.svelte';

	export let numberValue: number;

	const dispatch = createEventDispatcher<{
		selected: { value: number; label: string };
	}>();

	let options: { value: number; label: string }[] = [];
	let value = 0;

	$slices.forEach((s) => {
		options.push({ value: s.id, label: s.sliceName });
	});
	value = numberValue;

	function valueSelected(e: CustomEvent) {
		if (e.detail.value !== numberValue) {
			dispatch('selected', e.detail);
		}
	}
</script>

<EncodingContainer>
	<Svelecte style="width: 280px; flex:none;" bind:value {options} on:change={valueSelected} />
</EncodingContainer>
