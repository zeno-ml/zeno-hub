<script lang="ts">
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import { Icon } from '@smui/icon-button';

	export let pageName: string;
	export let tooltipContent: string;
	export let icon: string;
</script>

<button
	class="m-auto flex cursor-pointer items-center p-3 hover:bg-black-transparent"
	on:click
	use:tooltip={{ text: tooltipContent }}
	aria-label={pageName}
>
	<div class="h-6 w-6 fill-grey">
		<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
			<path
				class={`${
					$page.url.href.includes(pageName) ||
					(pageName === 'home' && $page.url.href.split('/').length === 6)
						? 'fill-primary'
						: 'fill-grey'
				}`}
				d={icon}
			/>
		</Icon>
	</div>
</button>
