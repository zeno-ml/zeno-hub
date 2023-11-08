<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import type { User } from '$lib/zenoapi';
	import { mdiHeart, mdiHeartOutline } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { createEventDispatcher } from 'svelte';

	export let likes: number;
	export let liked: boolean;
	export let user: User | null;

	let hovering = false;

	const dispatch = createEventDispatcher();
</script>

<div class="ml-auto flex">
	<div class="flex">
		<p class="pr-2 text-base font-semibold text-grey-dark">{likes}</p>
		<button
			class=" h-6 w-6 fill-primary-dark"
			on:mouseover={() => (hovering = true)}
			on:mouseout={() => (hovering = false)}
			on:focus={() => (hovering = true)}
			on:blur={() => (hovering = false)}
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
				<path d={user === null || liked || hovering ? mdiHeart : mdiHeartOutline} />
			</Icon>
		</button>
	</div>
</div>
