<script lang="ts">
	import type { SeparatedValues } from '$lib/instance-views/schema.js';

	export let data: string;
	export let spec: SeparatedValues;

	const values = data.split('\n').map((x) => x.split(spec.separator as string));
</script>

{#each values as value}
	<div class="table-row {spec.highlight ? 'bg-grey-lighter' : ''}">
		{#if spec.header !== undefined}
			<div class="table-cell border border-grey-light p-2">{spec.header}</div>
		{/if}
		{#each value as cell}
			<div class="table-cell border border-grey-light p-2">
				{cell}
			</div>
		{/each}
	</div>
{/each}
