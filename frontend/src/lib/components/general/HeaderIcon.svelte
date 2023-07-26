<script lang="ts">
	import { page } from '$app/stores';
	import { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';

	export let pageName: string;
	export let tooltipContent: string;
	export let icon: string;
</script>

<button
	class="m-auto flex items-center cursor-pointer p-3 hover:bg-black-transparent {$page.url.href.includes(
		pageName
	)
		? 'font-medium'
		: ''}"
	on:click
	use:tooltip={{
		content: tooltipContent,
		position: 'right',
		theme: 'zeno-tooltip'
	}}
>
	<div class="w-6 h-6 fill-grey">
		<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
			<path
				class={`${$page.url.href.includes(pageName) ? 'fill-primary' : 'fill-grey'}`}
				d={icon}
			/>
		</Icon>
	</div>
</button>
