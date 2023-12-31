<script lang="ts">
	import { goto } from '$app/navigation';
	import { navigating, page } from '$app/stores';
	import { tooltip } from '$lib/util/tooltip';
	import type { Project, Report, User, ZenoService } from '$lib/zenoapi';
	import {
		mdiCog,
		mdiCompassOutline,
		mdiFileChartOutline,
		mdiHome,
		mdiLinkVariant,
		mdiPlus,
		mdiViewGridOutline
	} from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import CircleIconButton from './CircleIconButton.svelte';
	import HelpButton from './HelpButton.svelte';
	import LikeButton from './LikeButton.svelte';
	import Spinner from './Spinner.svelte';
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

	$: exploreTab = $page.route.id === '/(app)/home';
</script>

<div
	class="{project
		? 'border-b border-grey-lighter bg-yellowish-light px-3'
		: 'px-6'} flex h-16 w-full flex-shrink-0 flex-col items-center justify-between sm:flex-row"
>
	<div class="flex h-full w-full items-center">
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
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6">
					<path d={mdiFileChartOutline} />
				</svg>
				<h4 class="ml-1 mr-6 text-lg">{report.name}</h4>
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
				class="ml-5 mr-2 w-6 flex-shrink-0"
			>
				<path d={mdiViewGridOutline} />
			</svg>
			{#if project.description}
				<h1
					class="mr-6 overflow-ellipsis whitespace-nowrap text-lg"
					use:tooltip={{ text: project.description }}
					style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;"
				>
					{project.name}
				</h1>
			{:else}
				<h1
					class="mr-6 overflow-ellipsis whitespace-nowrap text-lg"
					style="max-width: 100%; overflow: hidden; text-overflow: ellipsis;"
				>
					{project.name}
				</h1>
			{/if}
			<LikeButton
				on:like={() => (project ? zenoClient.likeProject(project.uuid) : '')}
				{user}
				likes={numLikes}
				liked={userLiked}
				report={false}
			/>
		{/if}
		{#if project || report}
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
		{/if}
		{#if linkCopied}
			<p class="ml-2 text-grey-dark" transition:fade>Link copied to clipboard</p>
		{/if}
	</div>
	<div class="hidden h-full shrink-0 items-center sm:flex">
		{#if $navigating}
			<div class="mr-2">
				<Spinner width={26} height={26} />
			</div>
		{/if}
		<HelpButton />
		{#if (report && report.editor) || (project && project.editor)}
			<CircleIconButton icon={mdiCog} on:click={() => (editPopup = true)} positioning="mr-2" />
		{/if}
		{#if user && $page.route.id?.startsWith('/(app)/home')}
			<button
				class="mr-2 flex h-8 w-8 cursor-pointer items-center justify-center rounded-full border border-grey-light text-primary transition hover:bg-primary-mid"
				on:click={() => (exploreTab ? goto('/home/' + user?.name) : goto('/home'))}
				use:tooltip={{ text: exploreTab ? 'Home' : 'Explore' }}
			>
				<Icon tag="svg" viewBox="0 0 24 24" class="w-5 fill-primary">
					<path d={exploreTab ? mdiHome : mdiCompassOutline} />
				</Icon>
			</button>
		{/if}
		<UserButton {user} />
	</div>
</div>
