<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import CopyProjectPopup from '$lib/components/popups/CopyProjectPopup.svelte';
	import { clickOutside } from '$lib/util/clickOutside';
	import { tooltip } from '$lib/util/tooltip';
	import { shortenNumber } from '$lib/util/util';
	import type { Project, ProjectStats, Report, ReportStats, User, ZenoService } from '$lib/zenoapi';
	import {
		mdiAccountCircleOutline,
		mdiDatabaseOutline,
		mdiDotsHorizontal,
		mdiFileChartOutline,
		mdiLandRowsHorizontal,
		mdiRobotOutline,
		mdiViewGridOutline
	} from '@mdi/js';
	import { Icon } from '@smui/button';
	import { createEventDispatcher, getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';
	import EntryOptions from './EntryOptions.svelte';
	import EntryStat from './EntryStat.svelte';

	export let entry: Project | Report;
	export let stats: ProjectStats | ReportStats;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const dispatch = createEventDispatcher();

	const project = 'uuid' in entry ? (entry as Project) : null;
	const report = 'id' in entry ? (entry as Report) : null;
	const projectStats = 'uuid' in entry ? (stats as ProjectStats) : null;
	const reportStats = 'id' in entry ? (stats as ReportStats) : null;
	const exploreTab = $page.route.id === '/(app)/home';

	let showOptions = false;
	let hovering = false;
	let showCopy = false;
	let showConfirmDelete = false;

	function deleteEntry() {
		if (project !== null) {
			zenoClient.deleteProject(project.uuid).then(() => dispatch('deleted'));
		} else if (report !== null) {
			zenoClient.deleteReport(report.id).then(() => dispatch('deleted'));
		}
		showConfirmDelete = false;
	}

	function likeEntry() {
		if (project !== null) {
			zenoClient.likeProject(project.uuid);
		} else if (report !== null) {
			zenoClient.likeReport(report.id);
		}
	}
</script>

{#if showCopy && user !== null && project !== null}
	<CopyProjectPopup config={project} on:close={() => (showCopy = false)} {user} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message={`Are you sure you want to delete this ${project ? 'project' : 'report'}?`}
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => deleteEntry()}
	/>
{/if}
<button
	on:click={() =>
		goto(
			`/${project ? 'project' : 'report'}/${
				project ? project.uuid : report?.id
			}/${encodeURIComponent(entry.name)}`
		)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => {
		hovering = false;
		showOptions = false;
	}}
	on:blur={() => {
		hovering = false;
		showOptions = false;
	}}
	class="flex h-full w-full flex-col rounded-md border border-solid border-grey-light bg-white hover:shadow-sm"
>
	<div
		class="relative flex w-full flex-col rounded-t-md text-center align-middle"
		style="background: {project ? '#f6f5f6' : '#f9f2ff'}"
	>
		<div class="mt-2 flex h-9 w-full items-center justify-between px-3">
			<div class="flex items-center justify-center">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					class="w-6 {report ? 'fill-primary-dark' : 'fill-grey-dark'}"
				>
					<path d={project ? mdiViewGridOutline : mdiFileChartOutline} />
				</svg>
				<div
					class="relative ml-2"
					use:clickOutside={() => {
						showOptions = false;
					}}
				>
					{#if hovering && (project || (project && !exploreTab) || (report && !exploreTab && user?.name === entry.ownerName))}
						<button
							class="rounded-md hover:bg-primary-mid"
							on:click={(e) => {
								e.stopPropagation();
								showOptions = !showOptions;
							}}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								class="w-6 fill-primary-dark"
							>
								<path fill="black" d={mdiDotsHorizontal} />
							</svg>
						</button>
					{/if}
					{#if showOptions}
						<EntryOptions
							bind:showOptions
							bind:showConfirmDelete
							bind:showCopy
							{report}
							{project}
							{user}
						/>
					{/if}
				</div>
			</div>
			<LikeButton on:like={likeEntry} likes={stats.numLikes} liked={stats.userLiked} {user} />
		</div>
		<div
			class="mb-4 mt-1 flex max-h-[3rem] min-h-[60px] items-center justify-center px-2"
			use:tooltip={{ text: entry.name }}
		>
			<p class="line-clamp-2 text-xl text-black">
				{entry.name}
			</p>
		</div>
	</div>
	<div class="flex w-full items-center justify-between pb-3 pl-2 pt-3">
		<div class="flex items-center">
			<Icon class="mr-2 h-6 w-6" tag="svg" viewBox="0 0 24 24">
				<path class="fill-grey-dark" d={mdiAccountCircleOutline} />
			</Icon>
			<p class="flex-shrink-0 truncate text-base text-grey-dark">{entry.ownerName}</p>
		</div>
		<div class="flex items-center rounded-md">
			{#if projectStats !== null}
				<EntryStat
					icon={mdiDatabaseOutline}
					text={projectStats.numInstances}
					tooltipContent={`This project has ${shortenNumber(
						projectStats.numInstances,
						1
					)} data point${projectStats.numInstances !== 1 ? 's' : ''}.`}
				/>
				<EntryStat
					icon={mdiRobotOutline}
					text={projectStats.numModels}
					tooltipContent={`This project has ${shortenNumber(projectStats.numModels, 1)} system${
						projectStats.numModels !== 1 ? 's' : ''
					}.`}
				/>
			{:else if reportStats !== null}
				<EntryStat
					icon={mdiLandRowsHorizontal}
					text={reportStats.numElements}
					tooltipContent={`This report has ${shortenNumber(reportStats.numElements, 1)} element${
						reportStats.numElements !== 1 ? 's' : ''
					}.`}
				/>
			{/if}
		</div>
	</div>
	{#if entry.description}
		<div class="px-3 pb-3" use:tooltip={{ text: entry.description }}>
			<p class="line-clamp-3 w-full text-left text-sm">
				{entry.description}
			</p>
		</div>
	{/if}
</button>
