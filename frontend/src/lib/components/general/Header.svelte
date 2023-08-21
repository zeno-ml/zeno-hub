<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ProjectPopup from '$lib/components/popups/ProjectPopup.svelte';
	import { authToken, project } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import type { User } from '$lib/zenoapi';
	import {
		mdiAccount,
		mdiChartBoxOutline,
		mdiCog,
		mdiCompare,
		mdiCompassOutline,
		mdiLogout
	} from '@mdi/js';
	import HeaderIcon from './HeaderIcon.svelte';

	export let user: User;

	let projectEdit = false;
</script>

{#if projectEdit && $project}
	<ProjectPopup config={$project} on:close={() => (projectEdit = false)} {user} />
{/if}
<nav>
	<header class="h-full w-12 flex bg-yellowish justify-between flex-col text-grey items-center">
		<div class="flex flex-col items-center justify-center">
			<a href="/">
				<img class="w-8 mt-5" src="/zeno.png" alt="Square spiral logo next to 'Zeno'" />
			</a>
			{#if $page.url.href.includes('project')}
				<div class="flex flex-col mt-3">
					<HeaderIcon
						pageName={'explore'}
						tooltipContent={'Explore your data and model outputs.'}
						icon={mdiCompassOutline}
						on:click={() => goto(`${getProjectRouteFromURL($page.url)}/explore`)}
					/>
					<HeaderIcon
						pageName={'compare'}
						tooltipContent={'Qualitatively compare model outputs.'}
						icon={mdiCompare}
						on:click={() => goto(`${getProjectRouteFromURL($page.url)}/compare`)}
					/>
					<HeaderIcon
						pageName={'chart'}
						tooltipContent={'Create charts from your slices and metrics.'}
						icon={mdiChartBoxOutline}
						on:click={() => goto(`${getProjectRouteFromURL($page.url)}/chart`)}
					/>
					{#if $project && $project.editor}
						<HeaderIcon
							pageName={'editProject'}
							tooltipContent={"Edit your project's configuration."}
							icon={mdiCog}
							on:click={() => (projectEdit = true)}
						/>
					{/if}
				</div>
			{/if}
		</div>

		<div class="m-auto flex flex-col items-center justify-center mb-3">
			<HeaderIcon
				pageName={'account'}
				tooltipContent={'Manage your account.'}
				icon={mdiAccount}
				on:click={() => goto(`/account`)}
			/>
			<form method="POST" action="/logout">
				<HeaderIcon
					pageName={'logout'}
					tooltipContent={'Logout.'}
					icon={mdiLogout}
					on:click={() => authToken.set(undefined)}
				/>
			</form>
		</div>
	</header>
</nav>
