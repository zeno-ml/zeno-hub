<script lang="ts">
	import { tooltip } from '$lib/util/tooltip';
	import type { Project, User, ZenoService } from '$lib/zenoapi';
	import { mdiLinkVariant } from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import LikeButton from '../general/LikeButton.svelte';
	import UserButton from '../general/UserButton.svelte';

	export let project: Project;
	export let likes: number;
	export let liked: boolean;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let linkCopied = false;
</script>

<div
	class="flex w-full min-w-0 shrink-0 items-center justify-between overflow-hidden border-b border-b-grey-lighter bg-yellowish-light px-3 py-1"
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
		<IconButton
			class="ml-2"
			on:click={(e) => {
				e.stopPropagation();
				linkCopied = true;
				navigator.clipboard.writeText(window.location.href.split('/explore')[0]);
				setTimeout(() => (linkCopied = false), 2000);
			}}
		>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={mdiLinkVariant} />
			</Icon>
		</IconButton>
		{#if linkCopied}
			<p class="ml-2 text-grey-dark" transition:fade>Project link copied to clipboard</p>
		{/if}
	</div>
	<UserButton {user} />
</div>
