<script lang="ts">
	import { elementMap } from '$lib/instance-views/resolve.js';
	import type { List, ViewUnion } from '$lib/instance-views/schema.js';
	import { mdiChevronDown, mdiChevronLeft, mdiChevronRight, mdiChevronUp } from '@mdi/js';
	import Error from '../Error.svelte';

	export let data: string;
	export let spec: List;

	let jsonData: Array<ViewUnion> | undefined = undefined;
	let errorMessage: string | undefined = undefined;

	$: showAll = jsonData !== undefined ? jsonData.length <= 5 : false;

	$: try {
		jsonData = JSON.parse(data);
		errorMessage = undefined;
		if (!Array.isArray(jsonData)) {
			jsonData = undefined;
			errorMessage = 'Data is not an array';
		}
	} catch (error) {
		jsonData = undefined;
		errorMessage = error as string;
	}

	$: shownDocs =
		jsonData === undefined
			? []
			: showAll || spec.collapsible === undefined
			? jsonData
			: spec.collapsible === 'bottom'
			? jsonData.slice(0, 4)
			: jsonData.slice(-4);
</script>

{#if jsonData === undefined}
	<Error type="Incorrect Data" message={errorMessage} />
{:else}
	<div class="flex {spec.horizontal ? 'flex-row' : 'flex-col'}">
		{#if spec.collapsible === 'top' && jsonData.length > 4}
			<button
				class="bg-transparent flex cursor-pointer items-center self-center rounded-2xl p-1 hover:bg-grey-lighter"
				on:click={() => (showAll = !showAll)}
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
					{#if spec.horizontal}
						<path d={showAll ? mdiChevronLeft : mdiChevronRight} />
					{:else}
						<path d={showAll ? mdiChevronDown : mdiChevronUp} />
					{/if}
				</svg>
				<span class="pr-1">Show {showAll ? 'Less' : 'All'}</span>
			</button>
		{/if}
		{#each shownDocs as element (element)}
			<div
				class="rounded-sm {spec.pad ? 'p-3' : ''} {spec.border
					? 'border border-grey-lighter'
					: ''} m-1"
			>
				{#if spec.elements && spec.elements.type && typeof spec.elements.type === 'string'}
					<svelte:component
						this={elementMap[spec.elements.type]}
						spec={spec.elements}
						data={typeof element === 'object' ? JSON.stringify(element) : element}
					/>
				{:else}
					<Error type="Incorrect View Specification" message="No element type specified" />
				{/if}
			</div>
		{/each}
		{#if spec.collapsible === 'bottom'}
			<button
				class="bg-transparent flex cursor-pointer items-center self-center rounded-2xl p-1 hover:bg-grey-lighter"
				on:click={() => (showAll = !showAll)}
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
					{#if spec.horizontal}
						<path d={showAll ? mdiChevronLeft : mdiChevronRight} />
					{:else}
						<path d={showAll ? mdiChevronDown : mdiChevronUp} />
					{/if}
				</svg>
				<span class="pr-1">Show {showAll ? 'Less' : 'All'}</span>
			</button>
		{/if}
	</div>
{/if}
