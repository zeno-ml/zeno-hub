<script lang="ts">
	import { page } from '$app/stores';
	import { mdiArrowCollapseLeft } from '@mdi/js';
	import { SmuiElement } from '@smui/common';

	export let updateChart: () => void = () => {
		// Do nothing
	};

	let isHover = false;
</script>

<a
	class="flex cursor-pointer items-center"
	href={$page.url.href.split('?')[0].substring(0, $page.url.href.lastIndexOf('/'))}
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
	<SmuiElement
		tag="svg"
		style="width: 24px; height: 24px; padding-right: 10px"
		viewBox="-2 -2 26 26"
	>
		<path class="fill-{isHover ? 'black' : 'grey-dark'}" d={mdiArrowCollapseLeft} />
	</SmuiElement>
	<h4 class="text-grey-dark hover:text-black">Back to Chart Home</h4>
</a>
