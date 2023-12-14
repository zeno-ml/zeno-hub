<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Element from '$lib/components/project/home/Element.svelte';
	import { metrics, models } from '$lib/stores';

	export let data;

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}
</script>

<div class="relative h-full w-full">
	{#each data.elements as element}
		<div
			class="absolute overflow-auto p-2"
			style="width: {element.width}%; height: {element.height}%; top: {element.yPos}%; left: {element.xPos}%;"
		>
			<div class="h-full w-full p-4">
				<Element {element} />
			</div>
		</div>
	{/each}
</div>
