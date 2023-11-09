<script lang="ts">
	import { tooltipState } from '$lib/stores';
	import { fade } from 'svelte/transition';

	let windowWidth = 0;
	let windowHeight = 0;
	let tooltipWidth = 0;
	let tooltipHeight = 0;

	$: yPos =
		windowHeight > $tooltipState.mousePos.y + tooltipHeight + 20
			? $tooltipState.mousePos.y
			: $tooltipState.mousePos.y - tooltipHeight - 20;
	$: xStyle =
		windowWidth > $tooltipState.mousePos.x + tooltipWidth + 10
			? `left: ${$tooltipState.mousePos.x}px;`
			: `right: 10px;`;
	$: style = `top: ${yPos}px; ${xStyle}; max-width: 50%`;
</script>

<svelte:window bind:innerWidth={windowWidth} bind:innerHeight={windowHeight} />
{#if $tooltipState.hover && $tooltipState.text !== undefined}
	<div
		class="fixed z-30 my-4 flex rounded bg-yellowish-light p-1 text-sm text-grey shadow"
		{style}
		transition:fade
		bind:offsetWidth={tooltipWidth}
		bind:offsetHeight={tooltipHeight}
	>
		<div class="flex flex-col break-all p-2">
			{$tooltipState.text}
		</div>
	</div>
{/if}
