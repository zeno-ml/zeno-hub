<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { fade } from 'svelte/transition';

	export let user: User | null;

	const exploreTab = $page.route.id === '/(app)/home';

	let docsLink = 'https://zenoml.com/docs/intro';
	let showOptions = false;
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
		<button
			class="mr-3 h-8 w-8 rounded-full border border-grey-light text-xl capitalize text-primary transition hover:bg-primary-dark"
			use:tooltip={{ text: 'Help' }}
			on:click={() => (showOptions = !showOptions)}
		>
			?
		</button>
		<button
			class="h-8 w-8 rounded-full bg-primary font-extrabold capitalize text-white transition hover:bg-primary-dark"
			use:tooltip={{ text: 'My Account' }}
			on:click={() => goto('/account')}
		>
			{user.name.slice(0, 2)}
		</button>
	{:else}
		<div class="h-8">
			<Button class="mr-3 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		</div>
	{/if}
	{#if showOptions}
		<button
			class="absolute right-14 top-12 z-50"
			transition:fade={{ duration: 100 }}
			use:clickOutside={() => (showOptions = !showOptions)}
			on:click={(e) => e.stopPropagation()}
			on:keydown={(e) => {
				if (e.key === 'Escape') {
					showOptions = false;
				}
			}}
		>
			<Paper style="padding: 7px 0px 7px 0px;" elevation={7}>
				<Content>
					<button
						class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
						on:keydown={() => ({})}
						on:click={(e) => {
							e.stopPropagation();
							if (browser) window.open('https://github.com/zeno-ml/zeno-hub/issues', '_blank');
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">bug_report</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Report an Issue</span>
					</button>
					<button
						class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
						on:keydown={() => ({})}
						on:click={(e) => {
							e.stopPropagation();
							if (browser) location.href = 'mailto:hello@zenoml.com';
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">mail</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Ask a Question</span>
					</button>
					<button
						class="mx-2 flex cursor-pointer items-center hover:bg-grey-lighter"
						on:keydown={() => ({})}
						on:click={(e) => {
							e.stopPropagation();
							if (browser) window.open(docsLink, '_blank');
							showOptions = false;
						}}
					>
						<Icon style="font-size: 20px;" class="material-icons">article</Icon>&nbsp;
						<span class="whitespace-nowrap text-sm">Explore the Docs</span>
					</button>
				</Content>
			</Paper>
		</button>
	{/if}
</div>
