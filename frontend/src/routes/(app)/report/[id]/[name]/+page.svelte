<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import Header from '$lib/components/general/Header.svelte';
	import Help from '$lib/components/general/Help.svelte';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import ReportPopup from '$lib/components/popups/ReportPopup.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import { svelecteRendererName } from '$lib/util/util.js';
	import { ReportElementType, ZenoService, type Project } from '$lib/zenoapi';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';

	export let data;

	let reportEdit = false;
	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let editId = -1;
	let showConfirmDelete = -1;

	const zenoClient = getContext('zenoClient') as ZenoService;

	function deleteElement(elementId: number) {
		if (elementId < 0) return;
		elements = elements.filter((e) => e.id !== elementId);
		zenoClient.deleteReportElement(data.report.id, elementId);
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
		invalidate('app:report');
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

<div class="absolute bottom-6 right-6">
	<Help />
</div>

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

<div class="flex h-full min-h-0 w-full min-w-0 flex-grow flex-col">
	<Header
		user={data.user}
		report={data.report}
		numLikes={data.numLikes}
		userLiked={data.userLiked}
		bind:reportEdit
	/>
	<div class="overflow-auto">
		<div
			class="m-auto flex w-full max-w-4xl flex-col rounded bg-background px-6 pb-20 pt-4 sm:mb-0 sm:mt-0 md:mb-6"
		>
			<h1 class="text-grey-darkest mr-6 pt-4 text-5xl">
				{data.report.name}
			</h1>
			<p class="mt-2 text-grey-dark">
				Updated {new Date(data.report.updatedAt ?? '').toLocaleString('en-US', {
					weekday: 'long',
					year: 'numeric',
					month: 'long',
					day: 'numeric',
					hour: 'numeric',
					minute: 'numeric'
				})}
			</p>
			<div class="mt-4 flex items-center text-lg">
				<p class="mr-2 font-medium text-grey-dark">Author:</p>
				<p>
					{data.report.ownerName}
				</p>
			</div>

			<div class="mt-2 flex w-full items-center">
				<p class="mr-2 text-lg font-medium text-grey-dark">Linked Projects:</p>
				{#if data.report.editor}
					{#await zenoClient.getUserProjects() then projects}
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
				{:else}
					<div class="flex">
						{#each data.projects as project}
							<button
								class="mr-1 flex w-fit items-center rounded bg-primary-light px-2 py-1 font-medium transition hover:bg-primary-mid"
								on:click={() =>
									goto(`/project/${project.uuid}/${encodeURIComponent(project.name)}`)}
							>
								<img src="/zeno-logo-small.svg" alt="Zeno logo" class="mr-1" />
								<p class="mr-1">{project.name}</p>
							</button>
						{/each}
					</div>
				{/if}
			</div>
			{#if data.report.editor}
				<hr class="mb-4 mt-4 text-grey-light" />
				<AddElementButton
					position={0}
					{addElement}
					alwaysShow={elements.length === 0 ? true : false}
				/>
			{/if}
			<div class="mt-4 flex flex-col">
				{#each elements as element (element.id)}
					{#if data.report.editor}
						<div
							on:dblclick={() => (editId = element.id || -1)}
							aria-label="double-click to edit"
							role="button"
							tabindex="0"
						>
							<ElementContainer
								bind:element
								bind:editId
								bind:showConfirmDelete
								chartOptions={data.charts}
								sliceOptions={data.slices}
								tagOptions={data.tags}
								{swapElementPositions}
								{addElement}
								report={data.report}
							/>
						</div>
					{:else}
						<ElementContainer
							bind:element
							bind:editId
							bind:showConfirmDelete
							chartOptions={data.charts}
							sliceOptions={data.slices}
							tagOptions={data.tags}
							{swapElementPositions}
							{addElement}
							report={data.report}
						/>
					{/if}
				{/each}
			</div>
		</div>
	</div>
</div>
