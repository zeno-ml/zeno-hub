<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { collapseHeader, models, project } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import {
		mdiArrowCollapseLeft,
		mdiArrowCollapseRight,
		mdiChartBoxOutline,
		mdiCompare,
		mdiCompassOutline
	} from '@mdi/js';
	import HeaderIcon from '../general/HeaderIcon.svelte';

	$: currentTab = $page.url.href.split('/').pop();
</script>

<nav class="z-20 hidden md:flex">
	<header
		class="flex h-full w-12 flex-col items-center justify-between border-r border-x-grey-lighter bg-yellowish-light text-grey"
	>
		<div class="flex flex-col items-center justify-center">
			{#if $page.url.href.includes('project/')}
				<div class="flex flex-col">
					<HeaderIcon
						pageName={'explore'}
						tooltipContent={'Explore your data and system outputs'}
						icon={mdiCompassOutline}
						on:click={() => goto(getProjectRouteFromURL($page.url))}
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
			{/if}
		</div>
		<div class="flex h-full items-center">
			{#if currentTab?.includes('explore') || currentTab?.includes('compare')}
				<HeaderIcon
					pageName={'$collapseHeader'}
					tooltipContent={$collapseHeader ? 'Expand sidebar' : 'Collapse sidebar'}
					icon={$collapseHeader ? mdiArrowCollapseRight : mdiArrowCollapseLeft}
					on:click={() => collapseHeader.set(!$collapseHeader)}
				/>
			{/if}
		</div>
	</header>
</nav>
