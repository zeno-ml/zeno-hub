<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Element from '$lib/components/project/home/Element.svelte';
	import { metrics, models } from '$lib/stores';

	export let data;

	if ($models.length === 0 || $metrics.length === 0) {
		goto(`${$page.url.pathname}/explore`);
	}

	console.log(data.elements);
</script>

<div class="grid h-full min-h-0 w-full min-w-0 gap-4 bg-yellowish p-4">
	{#each data.elements as element}
		<div
			class="overflow-auto bg-white shadow"
			style="grid-column: {element.xPos} / span {element.width}; grid-row: {element.yPos} / span {element.width};"
		>
			<Element {element} />
		</div>
	{/each}
</div>
