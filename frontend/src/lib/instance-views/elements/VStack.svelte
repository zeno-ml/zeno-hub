<script lang="ts">
	import { elementMap } from '$lib/instance-views/resolve.js';
	import type { VStack, View } from '$lib/instance-views/schema.js';
	import Error from '../Error.svelte';

	export let data: string;
	export let spec: VStack;

	let jsonData: Record<string, View> | undefined = undefined;
	let errorMessage: string | undefined = undefined;

	$: try {
		jsonData = JSON.parse(data);
		errorMessage = undefined;
	} catch (error) {
		jsonData = undefined;
		errorMessage = error as string;
	}

	function resolveElementType(key: string) {
		return elementMap[spec.keys[key].type as string];
	}
</script>

{#if jsonData === undefined}
	<Error type="Incorrect Data" message={errorMessage} />
{:else}
	<div class="flex flex-col">
		{#each Object.keys(spec.keys) as key}
			{#if key in jsonData}
				<svelte:component
					this={resolveElementType(key)}
					spec={spec.keys[key]}
					data={typeof jsonData[key] === 'object' ? JSON.stringify(jsonData[key]) : jsonData[key]}
				/>
			{:else}
				<p class="text-error">ERROR: no data for key <b>{key}</b></p>
			{/if}
		{/each}
	</div>
{/if}
