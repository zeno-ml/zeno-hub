<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import Button from '@smui/button';

	export let user: User | null = null;
	export let showNewReport = false;

	const exploreTab = $page.route.id === '/(app)/home';
</script>

<div class="flex items-center justify-between">
	<div class="flex h-full items-center">
		<a href="/">
			<img src="/zeno-logo.png" class="h-8" alt="diamond tesselation logo" />
		</a>
		{#if $page.route.id?.startsWith('/(app)/home/')}
			<div class="flex h-full md:ml-2 md:mt-0">
				<Button class="h-full" on:click={() => (showNewReport = true)}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						class="mr-2 w-6 fill-primary-dark"
					>
						<path d={mdiPlus} />
					</svg>
					New Report
				</Button>
			</div>
		{/if}
	</div>
	<!-- round div with the first letter of the username in the middle -->
	<div class="flex h-full items-center">
		{#if user}
			{#if $page.route.id?.startsWith('/(app)/home')}
				<Button
					class="mr-3 h-full"
					variant="outlined"
					on:click={() => (exploreTab ? goto('/') : goto('/home'))}
					>{exploreTab ? 'My Hub' : 'Explore'}</Button
				>
			{/if}
			<button
				class="flex h-10 w-10 items-center justify-center rounded-full bg-primary-dark font-extrabold capitalize text-white"
				use:tooltip={{ text: 'Account Settings' }}
				on:click={() => goto('/account')}
			>
				{user.name[0]}
			</button>
		{:else}
			<Button class="mr-3 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="mr-3 h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		{/if}
	</div>
</div>
