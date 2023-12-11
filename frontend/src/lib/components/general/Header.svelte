<script lang="ts">
	import { page } from '$app/stores';
	import type { Report, User, ZenoService } from '$lib/zenoapi';
	import { mdiFileChartOutline, mdiLinkVariant, mdiPlus } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import LikeButton from './LikeButton.svelte';
	import UserButton from './UserButton.svelte';

	export let user: User | null = null;
	export let report: Report | null = null;
	export let showNewReport = false;
	export let numLikes = 0;
	export let userLiked = false;
	export let reportEdit = false;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let linkCopied = false;
</script>

<div class="mx-6 my-5 flex h-8 items-center justify-between">
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
					report={report ? true : false}
				/>
				<IconButton
					class="ml-2"
					on:click={(e) => {
						e.stopPropagation();
						linkCopied = true;
						navigator.clipboard.writeText(window.location.href);
						setTimeout(() => (linkCopied = false), 2000);
					}}
				>
					<Icon tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiLinkVariant} />
					</Icon>
				</IconButton>
				{#if linkCopied}
					<p class="ml-2 text-grey-dark" transition:fade>Report link copied to clipboard</p>
				{/if}
			</div>
		{/if}
	</div>
	<div class="flex h-full shrink-0 items-center">
		{#if report && report.editor}
			<Button
				class="mr-4 mt-2 shrink-0 sm:mt-0"
				variant="outlined"
				on:click={() => (reportEdit = true)}>Settings</Button
			>
		{/if}
		<UserButton {user} />
	</div>
</div>
