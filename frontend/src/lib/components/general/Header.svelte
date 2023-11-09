<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import { mdiFileChartOutline, mdiPlus } from '@mdi/js';
	import Button from '@smui/button';

	export let user: User | null = null;
	export let showNewReport = false;
	export let reportTitle = '';

	const exploreTab = $page.route.id === '/(app)/home';
</script>

<div class="flex h-8 items-center justify-between">
	<div class="flex h-full items-center">
		<a href="/" class="shrink-0">
			<img src="/zeno-logo.png" class="h-8" alt="diamond tesselation logo" />
		</a>
		{#if $page.route.id?.startsWith('/(app)/home/')}
			<div class="flex h-full md:ml-2 md:mt-0">
				<Button class="h-full" on:click={() => (showNewReport = true)}>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 w-6 fill-primary">
						<path d={mdiPlus} />
					</svg>
					New Report
				</Button>
			</div>
		{/if}
		{#if reportTitle}
			<div class="ml-5 hidden items-center sm:flex">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class=" w-6 fill-grey-dark">
					<path d={mdiFileChartOutline} />
				</svg>
				<p class="ml-2 text-grey-dark">{reportTitle}</p>
			</div>
		{/if}
	</div>
	<!-- round div with the first letter of the username in the middle -->
	<div class="flex h-full shrink-0 items-center">
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
				class="flex h-10 w-10 items-center justify-center rounded-full bg-primary-dark font-extrabold capitalize text-white transition hover:bg-primary"
				use:tooltip={{ text: 'Account Settings' }}
				on:click={() => goto('/account')}
			>
				{user.name[0]}
			</button>
		{:else}
			<Button class="mr-3 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		{/if}
	</div>
</div>
