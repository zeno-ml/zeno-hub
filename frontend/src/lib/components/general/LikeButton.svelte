<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import type { User } from '$lib/zenoapi';
	import { mdiHeart, mdiHeartOutline } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { createEventDispatcher } from 'svelte';

	export let likes: number;
	export let liked: boolean;
	export let user: User | null;
	export let report = false;
	export let tooltipPos = 'bottom';

	const dispatch = createEventDispatcher();
</script>

<div class="flex ml-auto">
	<Tooltip
		content={`Like this ${report ? 'report' : 'project'}!`}
		theme={'zeno-tooltip'}
		position={tooltipPos}
	>
		<div class="flex">
			<p class="mr-2 text-base font-semibold text-primary">{likes}</p>
			{#if user}
				<button
					class=" w-6 h-6 fill-primary"
					on:click={(e) => {
						e.stopPropagation();
						if (liked) {
							liked = false;
							likes = Math.max(0, likes - 1);
						} else {
							liked = true;
							likes++;
						}
						dispatch('like');
					}}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						<path d={liked ? mdiHeart : mdiHeartOutline} />
					</Icon>
				</button>
			{:else}
				<button
					class=" w-6 h-6 fill-primary"
					on:click={() => goto(`/login?redirectTo=${$page.url.pathname}`)}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						<path d={mdiHeart} />
					</Icon>
				</button>
			{/if}
		</div>
	</Tooltip>
</div>
