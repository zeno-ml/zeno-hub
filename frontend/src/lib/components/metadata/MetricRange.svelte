<script lang="ts">
	import { metric, metricRange, metrics } from '$lib/stores';

	function updateRange(e: Event, i: number) {
		const target = e.target as HTMLElement;

		let val = parseFloat(target.innerText);
		if (isNaN(val)) {
			target.innerText = $metricRange[i].toFixed(2);
			return;
		}

		metricRange.update((range) => {
			range[i] = val;
			return [...range];
		});
	}
</script>

{#if $metrics.length !== 0 && $metricRange[0] !== Infinity && $metricRange[0] !== null}
	<div class="flex items-center justify-end mr-1 text-grey-dark w-full overflow-hidden">
		<span class="mx-4 whitespace-nowrap overflow-hidden text-ellipsis">
			{$metric ? $metric.name : ''}
		</span>
		<span
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
		</span>
		<div class="w-10 h-4 mx-2.5 bg-gradient-to-r from-primary-light to-primary" />
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
