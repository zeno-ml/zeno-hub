<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { page } from '$app/stores';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import CopyProjectPopup from '$lib/components/popups/CopyProjectPopup.svelte';
	import { clickOutside } from '$lib/util/clickOutside';
	import { shortenNumber } from '$lib/util/util';
	import type { Project, ProjectStats, Report, ReportStats, User, ZenoService } from '$lib/zenoapi';
	import {
		mdiAccountCircleOutline,
		mdiDatabaseOutline,
		mdiDotsHorizontal,
		mdiFileTree,
		mdiRobotOutline,
		mdiSitemap
	} from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';
	import EntryOptions from './EntryOptions.svelte';
	import EntryStat from './EntryStat.svelte';

	export let entry: Project | Report;
	export let stats: ProjectStats | ReportStats;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;

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
			zenoClient.deleteProject(project.uuid).then(() => invalidate('app:projects'));
		} else if (report !== null) {
			zenoClient.deleteReport(report.id).then(() => invalidate('app:reports'));
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
		goto(`/${project ? 'project' : 'report'}/${entry.ownerName}/${encodeURIComponent(entry.name)}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="flex flex-col rounded-lg border border-solid border-grey-light px-4 py-2 shadow-sm hover:shadow-md"
>
	<div class="flex w-full items-center justify-between">
		<p class="truncate text-left text-lg text-black">{entry.name}</p>
		<div class="flex items-center">
			<div
				class="relative mr-2 h-9 w-9"
				use:clickOutside={() => {
					showOptions = false;
				}}
			>
				{#if hovering && (project || (project && !exploreTab) || (report && !exploreTab && user?.name === entry.ownerName))}
					<IconButton
						size="button"
						style="padding: 0px"
						on:click={(e) => {
							e.stopPropagation();
							showOptions = !showOptions;
						}}
					>
						<Icon tag="svg" viewBox="0 0 24 24">
							<path fill="black" d={mdiDotsHorizontal} />
						</Icon>
					</IconButton>
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
			<LikeButton
				on:like={likeEntry}
				likes={stats.numLikes}
				liked={stats.userLiked}
				{user}
				report
			/>
		</div>
	</div>
	<div class="mb-2 flex items-center">
		<Icon class="mr-2 h-6 w-6" tag="svg" viewBox="0 0 24 24">
			<path class="fill-grey-dark" d={mdiAccountCircleOutline} />
		</Icon>
		<p class="flex-shrink-0 truncate text-base text-grey-dark">{entry.ownerName}</p>
	</div>
	<p class="w-full flex-grow overflow-y-auto text-left text-sm">
		{#if entry.description}
			{entry.description.slice(0, 100)}
			{#if entry.description.length > 100}
				...
			{/if}
		{/if}
	</p>
	<div
		class="my-2 flex w-full items-center justify-between rounded-md px-4 py-2 {report
			? 'bg-primary'
			: 'bg-primary-light'}"
	>
		<div class="font-semibold {report ? 'text-white' : ''}">
			{project ? 'project' : 'report'}
		</div>
		<div class="flex items-center">
			{#if projectStats !== null}
				<EntryStat
					entryType={project ? 'project' : 'report'}
					icon={mdiDatabaseOutline}
					text={projectStats.numInstances}
					tooltipContent={`This project has ${shortenNumber(
						projectStats.numInstances,
						1
					)} data point${projectStats.numInstances !== 1 ? 's' : ''}.`}
				/>
				<EntryStat
					entryType={project ? 'project' : 'report'}
					icon={mdiRobotOutline}
					text={projectStats.numModels}
					tooltipContent={`This project has ${shortenNumber(projectStats.numModels, 1)} system${
						projectStats.numModels !== 1 ? 's' : ''
					}.`}
				/>
			{:else if reportStats !== null}
				<EntryStat
					entryType={project ? 'project' : 'report'}
					icon={mdiFileTree}
					text={reportStats.numProjects}
					tooltipContent={`This report has ${shortenNumber(reportStats.numProjects, 1)} project${
						reportStats.numProjects !== 1 ? 's' : ''
					} linked to it.`}
				/>
				<EntryStat
					entryType={project ? 'project' : 'report'}
					icon={mdiSitemap}
					text={reportStats.numElements}
					tooltipContent={`This report has ${shortenNumber(reportStats.numElements, 1)} element${
						reportStats.numElements !== 1 ? 's' : ''
					}.`}
				/>
			{/if}
		</div>
	</div>
</button>
