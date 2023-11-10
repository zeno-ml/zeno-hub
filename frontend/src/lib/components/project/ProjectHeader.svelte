<script lang="ts">
	import { goto } from '$app/navigation';
	import { tooltip } from '$lib/util/tooltip';
	import type { Project, User, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';

	export let project: Project;
	export let likes: number;
	export let liked: boolean;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<div
	class="flex w-full min-w-0 items-center justify-between overflow-hidden border-b border-b-grey-lighter bg-yellowish-light px-3 py-4"
>
	<div class="flex items-center">
		{#if project.description}
			<h1
				class="mr-6 truncate text-ellipsis text-xl font-semibold"
				use:tooltip={{ text: project.description }}
			>
				{project.name}
			</h1>
		{:else}
			<h1 class="mr-6 truncate text-ellipsis text-xl font-semibold">
				{project.name}
			</h1>
		{/if}
		<LikeButton on:like={() => zenoClient.likeProject(project.uuid)} {likes} {liked} {user} />
	</div>
	{#if user}
		<button
			class="flex h-8 w-8 items-center justify-center rounded-full bg-primary-dark font-extrabold capitalize text-white transition hover:bg-primary"
			use:tooltip={{ text: 'Account Settings' }}
			on:click={() => goto('/account')}
		>
			{user.name[0]}
		</button>
	{:else}
		<div class="h-8">
			<Button class="mr-3 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		</div>
	{/if}
</div>
