<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import { mdiHeart, mdiHeartOutline } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { createEventDispatcher } from 'svelte';

	export let likes: number;
	export let liked: boolean;
	export let user: User | null;
	export let report = false;

	const dispatch = createEventDispatcher();
</script>

<div class="flex">
	<div class="flex">
		<p class="pr-2 text-base font-semibold text-primary">{likes}</p>
		<button
			use:tooltip={{
				text: `${user === null ? 'Login to l' : 'L'}ike this ${report ? 'report' : 'project'}!`
			}}
			class=" h-6 w-6 fill-primary"
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
	</div>
</div>
