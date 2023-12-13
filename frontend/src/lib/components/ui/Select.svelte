<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let value: unknown;
	export let options: { value: unknown; label: string | number }[];

	let dispatch = createEventDispatcher();
</script>

<div class="relative">
	<select
		class="w-full appearance-none rounded border border-grey-light px-2 py-1.5 pe-8 outline-none transition ease-in-out"
		bind:value
		on:change={() => dispatch('change')}
	>
		{#each options as option}
			<option value={option.value}>{option.label}</option>
		{/each}
	</select>
	<span class="pointer-events-none absolute inset-y-0 right-0 ml-3 flex items-center pr-2">
		<svg class="text-gray-400 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
			<path
				fill-rule="evenodd"
				d="M10 3a.75.75 0 01.55.24l3.25 3.5a.75.75 0 11-1.1 1.02L10 4.852 7.3 7.76a.75.75 0 01-1.1-1.02l3.25-3.5A.75.75 0 0110 3zm-3.76 9.2a.75.75 0 011.06.04l2.7 2.908 2.7-2.908a.75.75 0 111.1 1.02l-3.25 3.5a.75.75 0 01-1.1 0l-3.25-3.5a.75.75 0 01.04-1.06z"
				clip-rule="evenodd"
			/>
		</svg>
	</span>
</div>
