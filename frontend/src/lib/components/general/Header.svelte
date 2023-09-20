<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ProjectPopup from '$lib/components/popups/ProjectPopup.svelte';
	import { authToken, collapseHeader, models, project } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import type { User } from '$lib/zenoapi';
	import {
		mdiAccount,
		mdiArrowCollapseLeft,
		mdiArrowCollapseRight,
		mdiChartBoxOutline,
		mdiCog,
		mdiCompare,
		mdiCompassOutline,
		mdiLogin,
		mdiLogout
	} from '@mdi/js';
	import HeaderIcon from './HeaderIcon.svelte';

	export let user: User | null;

	let projectEdit = false;

	$: currentTab = $page.url.href.split('/').pop();
</script>

{#if projectEdit && user !== null}
	<ProjectPopup config={$project} on:close={() => (projectEdit = false)} {user} />
{/if}
<nav class="z-20">
	<header
		class="h-full w-12 flex bg-white justify-between flex-col text-grey items-center border-r border-x-grey-lighter"
	>
		<div class="flex flex-col items-center justify-center">
			<a href="/">
				<img class="w-8 mt-5" src="/zeno.png" alt="Square spiral logo next to 'Zeno'" />
			</a>
			{#if $page.url.href.includes('project')}
				<div class="flex flex-col mt-3">
					<HeaderIcon
						pageName={'explore'}
						tooltipContent={'Explore your data and model outputs'}
						icon={mdiCompassOutline}
						on:click={() => goto(`${getProjectRouteFromURL($page.url)}/explore`)}
					/>
					{#if $models.length > 1}
						<HeaderIcon
							pageName={'compare'}
							tooltipContent={'Qualitatively compare model outputs'}
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
		<div class="flex flex-col items-center justify-center mb-3">
			{#if (currentTab?.includes('explore') || currentTab?.includes('compare') || currentTab?.includes('chart')) && $project?.ownerName === user?.name}
				<HeaderIcon
					pageName={'editProject'}
					tooltipContent={"Edit your project's configuration"}
					icon={mdiCog}
					on:click={() => (projectEdit = true)}
				/>
			{/if}
			{#if $authToken}
				<HeaderIcon
					pageName={'account'}
					tooltipContent={'Manage your account'}
					icon={mdiAccount}
					on:click={() => goto(`/account`)}
				/>
				<HeaderIcon
					pageName={'logout'}
					tooltipContent={'Logout'}
					icon={mdiLogout}
					on:click={() => {
						authToken.set(undefined);
						fetch('/logout', { method: 'POST' });
						location.reload();
					}}
				/>
			{:else}
				<HeaderIcon
					pageName={'login'}
					tooltipContent={'Login'}
					icon={mdiLogin}
					on:click={() => goto(`/login?redirect=${$page.url.href}`)}
				/>
			{/if}
		</div>
	</header>
</nav>
