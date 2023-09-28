<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let data;
</script>

<div class="flex flex-col w-full h-full p-6 pt-5 bg-yellowish">
	{#if data.cognitoUser !== null}
		<div class="flex text-3xl">
			<Tooltip content={'Your projects and reports'} theme={'zeno-tooltip'} position="bottom">
				<button
					class={`mr-6 ${
						!$page.url.href.includes('my') ? 'text-grey-dark' : ''
					} hover:text-primary`}
					on:click={() => goto('/my')}
				>
					My Hub
				</button>
			</Tooltip>
			<Tooltip content={'Public projects and reports'} theme={'zeno-tooltip'} position="bottom">
				<button
					class={`${!$page.url.href.includes('public') ? 'text-grey-dark' : ''} hover:text-primary`}
					on:click={() => goto('/public')}
				>
					Discover
				</button>
			</Tooltip>
		</div>
	{/if}
	<slot />
</div>
