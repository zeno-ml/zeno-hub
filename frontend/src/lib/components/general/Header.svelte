<script lang="ts">
	import { page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { Project, Report, User, ZenoService } from '$lib/zenoapi';
	import { mdiFileChartOutline, mdiLinkVariant, mdiPlus, mdiViewGridOutline } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import LikeButton from './LikeButton.svelte';
	import UserButton from './UserButton.svelte';

	export let user: User | null = null;
	export let report: Report | null = null;
	export let project: Project | null = null;
	export let showNewReport = false;
	export let numLikes = 0;
	export let userLiked = false;
	export let editPopup = false;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let linkCopied = false;
</script>

<div
	class="{project
		? 'border-b border-grey-lighter bg-yellowish-light px-3'
		: 'px-6'} flex h-16 flex-shrink-0 items-center justify-between"
>
	<div class="flex h-full items-center">
		<a href="/" class="shrink-0">
			<img src="/zeno-logo.png" class="h-8" alt="diamond tesselation logo" />
		</a>
		{#if $page.route.id?.startsWith('/(app)/home/')}
			<div class="flex h-full items-center md:ml-2 md:mt-0">
				<Button on:click={() => (showNewReport = true)}>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 w-6 fill-primary">
						<path d={mdiPlus} />
					</svg>
					New Report
				</Button>
			</div>
		{/if}
		{#if report}
			<div class="ml-5 hidden items-center sm:flex">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class=" w-6 fill-grey-dark">
					<path d={mdiFileChartOutline} />
				</svg>
				<p class="ml-1 mr-6 text-grey-dark">{report.name}</p>
				<LikeButton
					on:like={() => (report ? zenoClient.likeReport(report.id) : '')}
					{user}
					likes={numLikes}
					liked={userLiked}
					report={false}
				/>
			</div>
		{:else if project}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				class="ml-5 mr-2 w-6 fill-grey-dark"
			>
				<path d={mdiViewGridOutline} />
			</svg>
			{#if project.description}
				<p class="mr-6 text-grey-dark" use:tooltip={{ text: project.description }}>
					{project.name}
				</p>
			{:else}
				<p class="mr-6 text-grey-dark">{project.name}</p>
			{/if}
			<LikeButton
				on:like={() => (project ? zenoClient.likeProject(project.uuid) : '')}
				{user}
				likes={numLikes}
				liked={userLiked}
				report={false}
			/>
		{/if}
		<IconButton
			class="ml-2"
			on:click={(e) => {
				e.stopPropagation();
				linkCopied = true;
				if (project) {
					navigator.clipboard.writeText(window.location.href.split('/explore')[0]);
				} else {
					navigator.clipboard.writeText(window.location.href);
				}
				setTimeout(() => (linkCopied = false), 2000);
			}}
		>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={mdiLinkVariant} />
			</Icon>
		</IconButton>
		{#if linkCopied}
			<p class="ml-2 text-grey-dark" transition:fade>Link copied to clipboard</p>
		{/if}
	</div>
	<div class="flex h-full shrink-0 items-center">
		{#if (report && report.editor) || (project && project.editor)}
			<Button
				class="mr-4 mt-2 shrink-0 sm:mt-0"
				variant="outlined"
				on:click={() => (editPopup = true)}>Settings</Button
			>
		{/if}
		<UserButton {user} />
	</div>
</div>
