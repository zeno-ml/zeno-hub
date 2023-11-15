<script lang="ts">
	import Header from '$lib/components/general/Header.svelte';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import ReportPopup from '$lib/components/popups/ReportPopup.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import { svelecteRendererName } from '$lib/util/util.js';
	import { ReportElementType, ZenoService, type Project, type ReportElement } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { dndzone } from 'svelte-dnd-action';

	export let data;

	let reportEdit = false;
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

	function swapElementPositions(elementId: number | null | undefined, position: number) {
		if (!elementId || position < 0 || position >= elements.length) return;

		let currElement = elements.find((e) => e.id === elementId);
		let oldPosition = currElement?.position ?? -1;
		if (!currElement || oldPosition === position || oldPosition === -1) return;

		elements[position].position = oldPosition;
		currElement.position = position;

		zenoClient.updateReportElement(data.report.id, elements[position]);
		zenoClient.updateReportElement(data.report.id, currElement);

		elements.sort((a, b) => a.position - b.position);
		elements = [...elements];
	}
</script>

<svelte:window
	on:keydown={($event) => {
		if ($event.key === 'Escape') {
			editId = -1;
		}
	}}
/>
<svelte:head>
	<title>{data.report.name} | Zeno</title>
	<meta name="description" content={data.report.description || 'Zeno Evaluation Report'} />
</svelte:head>

{#if reportEdit && data.user !== null}
	<ReportPopup on:close={() => (reportEdit = false)} user={data.user} />
{/if}
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
<div class="relative h-screen w-full overflow-y-auto overflow-x-visible">
	<div class="sticky top-0 z-10 bg-white px-6 pt-6">
		<Header
			user={data.user}
			report={data.report}
			numLikes={data.numLikes}
			userLiked={data.userLiked}
			bind:reportEdit
		/>
	</div>
	<div
		class="m-auto flex max-w-4xl flex-col rounded bg-background px-6 pb-20 pt-4 sm:mb-0 sm:mt-0 md:mb-6"
	>
		<h1 class="text-grey-darkest mr-6 pt-4 text-5xl">
			{data.report.name}
		</h1>
		<div class="mt-4 flex items-center">
			<h5 class="text-lg">Author: {data.report.ownerName}</h5>
			<span class="ml-4 text-grey-darker"
				>Updated {new Date(data.report.updatedAt ?? '').toLocaleString('en-US', {
					weekday: 'long',
					year: 'numeric',
					month: 'long',
					day: 'numeric',
					hour: 'numeric',
					minute: 'numeric'
				})}</span
			>
		</div>
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
					renderer={svelecteRendererName}
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
					{element}
					bind:editId
					bind:dragEnabled
					bind:showConfirmDelete
					{swapElementPositions}
					{addElement}
					{selectedProjects}
					report={data.report}
				/>
			{/each}
		</div>
	</div>
</div>
