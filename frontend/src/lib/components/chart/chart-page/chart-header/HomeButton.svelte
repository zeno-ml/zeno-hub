<script lang="ts">
	import { page } from '$app/stores';
	import { mdiArrowCollapseLeft } from '@mdi/js';
	import { Svg } from '@smui/common';
	import { noop } from 'svelte/internal';

	export let updateChart: () => void = noop;

	let isHover = false;
</script>

<a
	class="flex items-center cursor-pointer mb-2"
	href={$page.url.href.substring(0, $page.url.href.lastIndexOf('/'))}
	on:click={updateChart}
	on:focus={() => ({})}
	on:mouseover={() => {
		isHover = true;
	}}
	on:blur={() => ({})}
	on:mouseout={() => {
		isHover = false;
	}}
>
	<Svg style="width: 24px; height: 24px; padding-right: 10px" viewBox="-2 -2 26 26">
		<path fill={isHover ? 'black' : 'var(--G2)'} d={mdiArrowCollapseLeft} />
	</Svg>
	<h4 class="text-grey-dark hover:text-black">Back to Chart Home</h4>
</a>
