<script lang="ts">
	import { metric, metricRange, metrics } from '$lib/stores';

	/**
	 * Updates the metric range.
	 * @param e Blur event from contenteditable div
	 * @param index 0 or 1 for whether this is the min or max element of the range
	 */
	function updateRange(e: Event, index: number) {
		const target = e.target as HTMLElement;

		let val = parseFloat(target.innerText);
		if (isNaN(val)) {
			target.innerText = $metricRange[index].toFixed(2);
			return;
		}

		metricRange.update((range) => {
			range[index] = val;
			return [...range];
		});
	}
</script>

{#if $metrics.length !== 0 && $metricRange[0] !== Infinity && $metricRange[0] !== null}
	<div class="mr-1 flex w-full items-center justify-end overflow-hidden text-grey-dark">
		<span class="mx-4 overflow-hidden text-ellipsis whitespace-nowrap">
			{$metric ? $metric.name : ''}
		</span>
		<div
			contenteditable="true"
			role="textbox"
			aria-label="Metric range min"
			tabindex="0"
			on:keydown={(e) => {
				if (e.key === 'Enter') {
					e.preventDefault();
					e.currentTarget.blur();
				}
			}}
			on:blur={(e) => updateRange(e, 1)}
		>
			{$metricRange[0].toFixed(2)}
		</div>
		<div class="mx-2.5 h-4 w-10 bg-gradient-to-r from-primary-light to-primary" />
		<div
			contenteditable="true"
			role="textbox"
			aria-label="Metric range max"
			tabindex="0"
			on:keydown={(e) => {
				if (e.key === 'Enter') {
					e.preventDefault();
					e.currentTarget.blur();
				}
			}}
			on:blur={(e) => updateRange(e, 1)}
		>
			{$metricRange[1].toFixed(2)}
		</div>
	</div>
{/if}
