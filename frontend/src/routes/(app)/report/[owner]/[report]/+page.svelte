<script lang="ts">
	import LikeButton from '$lib/components/general/LikeButton.svelte';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import { ReportElementType, ZenoService, type Project, type ReportElement } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let editId = -1;
	let showConfirmDelete = -1;
	let dragEnabled = false;

	const zenoClient = getContext('zenoClient') as ZenoService;

	function deleteElement(elementId: number) {
		if (elementId < 0) return;
		elements = elements.filter((e) => e.id !== elementId);
		zenoClient.deleteReportElement(elementId);
	}

	function addElement(elementIndex: number) {
		zenoClient
			.addReportElement(data.report.id, {
				type: ReportElementType.TEXT,
				data: 'new element',
				position: elementIndex
			})
			.then((res) => {
				elements.filter((d) => d.position >= elementIndex).forEach((d) => d.position++);
				elements.push({
					id: res,
					type: ReportElementType.TEXT,
					data: 'new element',
					position: elementIndex
				});
				elements = elements.sort((a, b) => a.position - b.position);
				editId = res;
			});
	}

	function updateReportProjects(e: CustomEvent) {
		const projectUuids = e.detail.map((p: Project) => p.uuid);
		zenoClient.updateReportProjects(data.report.id, projectUuids);
	}

	function handleDropped(e: CustomEvent) {
		e.detail.items.forEach((item: ReportElement, index: number) => {
			item.position = index;
			zenoClient.updateReportElement(data.report.id, { ...item, position: index });
		});
		elements = e.detail.items;
		dragEnabled = false;
	}

	function handleMoved(e: CustomEvent) {
		elements = e.detail.items;
	}
</script>

{#if showConfirmDelete !== -1}
	<Confirm
		message="Are you sure you want to delete this element?"
		on:cancel={() => {
			showConfirmDelete = -1;
		}}
		on:confirm={() => {
			deleteElement(showConfirmDelete);
			showConfirmDelete = -1;
		}}
	/>
{/if}
<div class="h-full w-full overflow-scroll bg-yellowish">
	<div
		class="m-auto flex max-w-4xl flex-col rounded bg-background px-10 pb-20 shadow sm:mb-0 sm:mt-0 md:mb-6 md:mt-6"
	>
		<div class="mt-12 flex items-center justify-between">
			<h1 class="text-grey-darkest mr-6 text-5xl">
				{data.report.name}
			</h1>
			<LikeButton
				on:like={() => zenoClient.likeReport(data.report.id)}
				user={data.user}
				likes={data.numLikes}
				liked={data.userLiked}
				report
			/>
		</div>
		<h5 class="ml-1 mt-4 text-lg">Author: {data.report.ownerName}</h5>
		<hr class="mt-4 text-grey-light" />

		{#if data.report.editor}
			<p class="mb-2 mt-4">Associated Projects</p>
			{#await zenoClient.getProjects() then projects}
				<Svelecte
					bind:value={selectedProjects}
					on:change={updateReportProjects}
					valueField="uuid"
					labelField="name"
					searchable={false}
					multiple={true}
					options={projects}
				/>
			{/await}
			<hr class="mb-4 mt-4 text-grey-light" />
			<AddElementButton
				position={0}
				{addElement}
				alwaysShow={elements.length === 0 ? true : false}
			/>
		{/if}
		<div
			class="mt-2 flex flex-col"
			use:dndzone={{
				items: elements,
				dragDisabled: !dragEnabled,
				dropTargetStyle: {},
				flipDurationMs: 100
			}}
			on:consider={handleMoved}
			on:finalize={handleDropped}
		>
			{#each elements as element (element.id)}
				<ElementContainer
					bind:element
					bind:editId
					bind:dragEnabled
					bind:showConfirmDelete
					{addElement}
					{selectedProjects}
					report={data.report}
				/>
			{/each}
		</div>
	</div>
</div>
