<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import { clickOutside } from '$lib/util/clickOutside';
	import { shortenNumber } from '$lib/util/util';
	import type { Project, ProjectStats, User, ZenoService } from '$lib/zenoapi';
	import { mdiDotsHorizontal, mdiImage, mdiLayersTriple, mdiTag, mdiText } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';
	import Confirm from '../popups/Confirm.svelte';
	import CopyProjectPopup from '../popups/CopyProjectPopup.svelte';
	import ProjectStat from './ProjectStat.svelte';

	export let project: Project;
	export let stats: ProjectStats;
	export let deletable = false;
	export let user: User | null = null;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let showOptions = false;
	let hovering = false;
	let showCopy = false;
	let showConfirmDelete = false;

	function getProjectIcon() {
		if (project.view.includes('image')) return mdiImage;
		if (project.view.includes('chat') || project.view.includes('text')) return mdiText;
		else return mdiTag;
	}
</script>

{#if showCopy && user !== null}
	<CopyProjectPopup config={project} on:close={() => (showCopy = false)} {user} />
{/if}
{#if showConfirmDelete}
	<Confirm
		message="Are you sure you want to delete this project?"
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => {
			zenoClient.deleteProject(project.uuid).then(() => invalidate('app:projects'));
			showConfirmDelete = false;
		}}
	/>
{/if}
<button
	on:click={() => goto(`/project/${project.ownerName}/${encodeURIComponent(project.name)}`)}
	on:mouseover={() => (hovering = true)}
	on:focus={() => (hovering = true)}
	on:mouseleave={() => (hovering = false)}
	on:blur={() => (hovering = false)}
	class="border-solid mr-2 mb-2 rounded-lg border-grey-light border shadow-sm flex flex-col p-3 px-5 hover:shadow-md w-full sm:w-80 h-60"
>
	<div class="flex flex-col w-full">
		<div class="flex justify-between items-center">
			<p class="mr-2 truncate text-black text-lg">{project.name}</p>
			<div
				class="w-9 h-9 relative"
				use:clickOutside={() => {
					showOptions = false;
				}}
			>
				{#if hovering && user !== null}
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
								{#if deletable}
									<button
										class="flex items-center w-20 py px-2 hover:bg-grey-lighter"
										on:click={(e) => {
											e.stopPropagation();
											showOptions = false;
											showConfirmDelete = true;
										}}
									>
										<Icon style="font-size: 18px;" class="material-icons">delete_outline</Icon
										>&nbsp;
										<span class="text-xs">Remove</span>
									</button>
								{/if}
							</Content>
						</Paper>
					</div>
				{/if}
			</div>
		</div>
	</div>
	<p class="mr-2 text-base truncate flex-shrink-0">{project.ownerName}</p>
	<p class="my-2 mr-2 text-sm w-full text-left overflow-y-auto flex-grow">
		{project.description}
	</p>
	<div class="flex items-center w-full mb-2 mt-3">
		<Tooltip
			content={`This project has ${shortenNumber(stats.numInstances, 1)} data point${
				stats.numInstances !== 1 ? 's' : ''
			}.`}
			theme={'zeno-tooltip'}
			position="bottom"
		>
			<ProjectStat icon={getProjectIcon()} text={stats.numInstances} />
		</Tooltip>
		<Tooltip
			content={`This project has ${shortenNumber(stats.numModels, 1)} system${
				stats.numModels !== 1 ? 's' : ''
			}.`}
			theme={'zeno-tooltip'}
			position="bottom"
		>
			<ProjectStat icon={mdiLayersTriple} text={stats.numModels} />
		</Tooltip>
		<LikeButton
			on:like={() => zenoClient.likeProject(project.uuid)}
			{user}
			likes={stats.numLikes}
			liked={stats.userLiked}
		/>
	</div>
</button>
