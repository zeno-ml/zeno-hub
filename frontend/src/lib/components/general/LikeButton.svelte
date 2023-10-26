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
	<div class="flex">
		<p class="mr-2 text-base font-semibold text-primary">{likes}</p>
		<Tooltip
			content={`${user === null ? 'Login to l' : 'L'}ike this ${report ? 'report' : 'project'}!`}
			theme={'zeno-tooltip'}
			position={tooltipPos}
		>
			<button
				class=" w-6 h-6 fill-primary"
				on:click={(e) => {
					if (user) {
						e.stopPropagation();
						if (liked) {
							liked = false;
							likes = Math.max(0, likes - 1);
						} else {
							liked = true;
							likes++;
						}
						dispatch('like');
					} else {
						goto(`/login?redirectTo=${$page.url.pathname}`);
					}
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path d={user === null || liked ? mdiHeart : mdiHeartOutline} />
				</Icon>
			</button>
		</Tooltip>
	</div>
</div>
