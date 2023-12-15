<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import Button from '@smui/button';
	import HelpButton from './HelpButton.svelte';

	export let user: User | null;

	const exploreTab = $page.route.id === '/(app)/home';
</script>

<div class="flex h-full w-max items-center">
	{#if user}
		{#if $page.route.id?.startsWith('/(app)/home')}
			<Button
				class="mr-3 h-full"
				variant="outlined"
				on:click={() => (exploreTab ? goto('/') : goto('/home'))}
				>{exploreTab ? 'My Hub' : 'Explore'}</Button
			>
		{/if}
		<HelpButton />
		<button
			class="h-8 w-8 rounded-full bg-primary font-extrabold capitalize text-white transition hover:bg-primary-dark"
			use:tooltip={{ text: 'My Account' }}
			on:click={() => goto('/account')}
		>
			{user.name.slice(0, 2)}
		</button>
	{:else}
		<HelpButton />
		<div class="h-8">
			<Button class="mr-3 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		</div>
	{/if}
</div>
