<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ProjectPopup from '$lib/components/popups/ProjectPopup.svelte';
	import { collapseHeader, metrics, models, project } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import type { User } from '$lib/zenoapi';
	import {
		mdiArrowCollapseLeft,
		mdiArrowCollapseRight,
		mdiChartBoxOutline,
		mdiCogOutline,
		mdiCompare,
		mdiCompassOutline,
		mdiHomeOutline
	} from '@mdi/js';
	import HeaderIcon from '../general/HeaderIcon.svelte';

	export let user: User | null;

	let projectEdit = false;

	$: currentTab = $page.url.href.split('/').pop();
</script>

{#if projectEdit && user !== null}
	<ProjectPopup config={$project} on:close={() => (projectEdit = false)} {user} />
{/if}
<nav class="z-20 flex md:hidden">
	<header
		class="flex w-full flex-col items-center justify-between border-r border-x-grey-lighter bg-yellowish text-grey"
	>
		<a href="/">
			<img class="w-8 pb-2 pt-2" src="/zeno.png" alt="Square spiral logo next to 'Zeno'" />
		</a>
	</header>
</nav>
<div class="z-20 hidden md:flex">
	<div
		class="flex h-full w-12 flex-col items-center justify-between border-r border-x-grey-lighter bg-yellowish-light text-grey"
	>
		<div class="flex flex-col items-center justify-center">
			<a href="/">
				<img class="mt-3 w-8" src="/zeno.png" alt="Square spiral logo next to 'Zeno'" />
			</a>
			<div class="mt-3 flex flex-col">
				{#if $models.length > 0 && $metrics.length > 0}
					<HeaderIcon
						pageName={'home'}
						tooltipContent={'Summary landing page'}
						icon={mdiHomeOutline}
						on:click={() => goto(getProjectRouteFromURL($page.url))}
					/>
				{/if}
				<HeaderIcon
					pageName={'explore'}
					tooltipContent={'Explore your data and system outputs'}
					icon={mdiCompassOutline}
					on:click={() => goto(`${getProjectRouteFromURL($page.url)}/explore`)}
				/>
				{#if $models.length > 1 && $project.view !== ''}
					<HeaderIcon
						pageName={'compare'}
						tooltipContent={'Qualitatively compare system outputs'}
						icon={mdiCompare}
						on:click={() => goto(`${getProjectRouteFromURL($page.url)}/compare`)}
					/>
				{/if}
				<HeaderIcon
					pageName={'chart'}
					tooltipContent={'Create charts from your slices and metrics'}
					icon={mdiChartBoxOutline}
					on:click={() => goto(`${getProjectRouteFromURL($page.url)}/chart`)}
				/>
			</div>
		</div>
		<div>
			{#if currentTab?.includes('explore') || currentTab?.includes('compare')}
				<HeaderIcon
					pageName={'$collapseHeader'}
					tooltipContent={$collapseHeader ? 'Expand sidebar' : 'Collapse sidebar'}
					icon={$collapseHeader ? mdiArrowCollapseRight : mdiArrowCollapseLeft}
					on:click={() => collapseHeader.set(!$collapseHeader)}
				/>
			{/if}
		</div>
		<div class="mb-3 flex flex-col items-center justify-center">
			{#if $project?.ownerName === user?.name}
				<HeaderIcon
					pageName={'editProject'}
					tooltipContent={"Edit your project's configuration"}
					icon={mdiCogOutline}
					on:click={() => (projectEdit = true)}
				/>
			{/if}
		</div>
	</div>
</div>
