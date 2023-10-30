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
	$: style = `top: ${yPos}px; ${xStyle};`;
</script>

<svelte:window bind:innerWidth={windowWidth} bind:innerHeight={windowHeight} />
{#if $tooltipState.hover && $tooltipState.text !== undefined}
	<div
		class="bg-yellowish-light text-grey text-sm fixed p-1 rounded shadow z-30 flex my-4"
		{style}
		transition:fade
		bind:offsetWidth={tooltipWidth}
		bind:offsetHeight={tooltipHeight}
	>
		<div class="flex flex-col p-2 break-all">
			{$tooltipState.text}
		</div>
	</div>
{/if}
