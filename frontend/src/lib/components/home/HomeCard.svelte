<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { page } from '$app/stores';
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
	import Paper, { Content } from '@smui/paper';
	import { getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';
	import Confirm from '../popups/Confirm.svelte';
	import CopyProjectPopup from '../popups/CopyProjectPopup.svelte';
	import ElementStat from './ElementStat.svelte';

	export let entry: Project | Report;
	export let stats: ProjectStats | ReportStats;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;

	const entryType = 'uuid' in entry ? 'project' : 'report';
	const project = entryType === 'project' ? (entry as Project) : null;
	const report = entryType === 'report' ? (entry as Report) : null;
	const projectStats = entryType === 'project' ? (stats as ProjectStats) : null;
	const reportStats = entryType === 'report' ? (stats as ReportStats) : null;

	let deletable = user && $page.route.id === '/(app)/home/[user]';
	let showCopy = false;
	let showOptions = false;
	let hovering = false;
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
			zenoClient.likeProject(project.uuid).then(() => invalidate('app:projects'));
		} else if (report !== null) {
			zenoClient.likeReport(report.id).then(() => invalidate('app:reports'));
		}
	}
</script>

{#if showCopy && user !== null && project !== null}
	<CopyProjectPopup config={project} on:close={() => (showCopy = false)} {user} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message={`Are you sure you want to delete this ${entryType}?`}
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => deleteEntry()}
	/>
{/if}
<button
	on:click={() => goto(`/${entryType}/${entry.ownerName}/${encodeURIComponent(entry.name)}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="border-solid rounded-lg border-grey-light border shadow-sm py-2 px-4 hover:shadow-md flex flex-col"
>
	<div class="flex justify-between w-full mb-2">
		<div class={deletable ? 'mr-5' : ''}>
			<p class="text-black text-lg text-left">{entry.name}</p>
			<div class="flex items-center mt-1">
				<Icon class="w-6 h-6 mr-2" tag="svg" viewBox="0 0 24 24">
					<path class="fill-grey-dark" d={mdiAccountCircleOutline} />
				</Icon>
				<p class="text-base truncate flex-shrink-0 text-grey-dark">{entry.ownerName}</p>
			</div>
		</div>
		<div
			class="w-9 h-9 relative"
			use:clickOutside={() => {
				showOptions = false;
			}}
		>
			<LikeButton
				on:like={likeEntry}
				likes={stats.numLikes}
				liked={stats.userLiked}
				{user}
				report
			/>
			{#if hovering}
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
				<div class="top-0 right-0 absolute mt-9 hover:bg-grey-lighter z-30">
					<Paper style="padding: 3px 0px;" elevation={7}>
						<Content>
							{#if project}
								<button
									class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										showCopy = true;
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">content_copy</Icon>&nbsp;
									<span class="text-xs">Copy</span>
								</button>
							{/if}
							{#if deletable}
								<button
									class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
									on:click={(e) => {
										e.stopPropagation();
										showOptions = false;
										showConfirmDelete = true;
									}}
								>
									<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon>&nbsp;
									<span class="text-xs">Remove</span>
								</button>
							{/if}
						</Content>
					</Paper>
				</div>
			{/if}
		</div>
	</div>
	<p class="mb-2 text-sm w-full text-left overflow-y-auto flex-grow">
		{#if entry.description}
			{entry.description.slice(0, 100)}
			{#if entry.description.length > 100}
				...
			{/if}
		{/if}
	</p>
	<div
		class="flex items-center justify-between w-full py-2 px-4 mb-2 rounded-md {report
			? 'bg-primary'
			: 'bg-primary-light'}"
	>
		<div class="font-semibold {report ? 'text-white' : ''}">{entryType}</div>
		<div class="flex items-center">
			{#if projectStats !== null}
				<ElementStat
					{entryType}
					icon={mdiDatabaseOutline}
					text={projectStats.numInstances}
					tooltipContent={`This project has ${shortenNumber(
						projectStats.numInstances,
						1
					)} data point${projectStats.numInstances !== 1 ? 's' : ''}.`}
				/>
				<ElementStat
					{entryType}
					icon={mdiRobotOutline}
					text={projectStats.numModels}
					tooltipContent={`This project has ${shortenNumber(projectStats.numModels, 1)} system${
						projectStats.numModels !== 1 ? 's' : ''
					}.`}
				/>
			{:else if reportStats !== null}
				<ElementStat
					{entryType}
					icon={mdiFileTree}
					text={reportStats.numProjects}
					tooltipContent={`This report has ${shortenNumber(reportStats.numProjects, 1)} project${
						reportStats.numProjects !== 1 ? 's' : ''
					} linked to it.`}
				/>
				<ElementStat
					{entryType}
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
