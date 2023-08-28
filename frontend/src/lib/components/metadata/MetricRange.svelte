<script lang="ts">
	import { metric, metricRange, metrics } from '$lib/stores';
</script>

{#if $metrics.length !== 0 && $metricRange[0] !== Infinity}
	<div class="flex items-center mr-1 text-grey-dark">
		<span class="mr-[15px]">
			{$metric ? $metric.name + ':' : ''}
		</span>
		<span
			contenteditable="true"
			on:blur={(e) =>
				metricRange.update((range) => {
					range[0] = parseFloat(e.currentTarget.innerText);
					return [...range];
				})}
		>
			{$metricRange[0].toFixed(2)}
		</span>
		<div class="w-10 h-4 mx-2.5 bg-gradient-to-r from-primary-light to-primary" />
		<span
			contenteditable="true"
			on:blur={(e) =>
				metricRange.update((range) => {
					range[1] = parseFloat(e.currentTarget.innerText);
					return [...range];
				})}
		>
			{$metricRange[1].toFixed(2)}
		</span>
	</div>
{/if}
