<script lang="ts">
	import type { TextView } from '$lib/instance-views/schema.js';

	export let data: string;
	export let spec: TextView;
</script>

{#if spec.label !== undefined}
	<p class="whitespace-pre-wrap text-grey">
		<span class="font-semibold">{spec.label}</span>
		{data}
	</p>
{:else}
	<p class="whitespace-pre-wrap text-grey">
		{data}
	</p>
{/if}
