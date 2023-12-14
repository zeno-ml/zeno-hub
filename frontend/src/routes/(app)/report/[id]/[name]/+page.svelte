<script lang="ts">
	import { goto, invalidate } from '$app/navigation';
	import Header from '$lib/components/general/Header.svelte';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import ReportPopup from '$lib/components/popups/ReportPopup.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import { svelecteRendererName } from '$lib/util/util.js';
	import {
		ReportElementType,
		ZenoService,
		type Author,
		type Project,
		type User
	} from '$lib/zenoapi';
	import { mdiAccountCircleOutline } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import Svelecte from 'svelecte';
	import { getContext } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';

	export let data;

	let reportEdit = false;
	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let authors: Author[] = data.authors.sort((a: Author, b: Author) => a.position - b.position);
	let selectedProjects = data.report.linkedProjects ?? [];
	let editId = -1;
	let showConfirmDelete = -1;
	let authorOptions: { id: number; label: string }[] = [
		...data.users.map((user: User) => {
			return {
				id: user.id,
				label: user.displayName
			};
		})
	];
	let authorsSelected: { id: number; label: string }[] = data.authors.map((author: Author) => {
		{
			return { id: author.user.id, label: author.user.displayName };
		}
	});

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

	$: updateReportAuthors(authorsSelected);

	function updateReportAuthors(authorsSelected: { id: number; label: string }[]) {
		const finalList: Author[] = [];
		authorsSelected.forEach((option: { id: number; label: string }, index: number) => {
			// Author not yet in list, add it
			if (!authors.map((author) => author.user.id).includes(option.id)) {
				const user = data.users.find((user: User) => user.id === option.id);
				if (user) {
					const author = { user: user, position: index };
					zenoClient.addReportAuthor(data.report.id, author);
					finalList.push(author);
				}
				// Author in wrong position, move it
			} else if (!authors[index] || option.id !== authors[index].user.id) {
				const user = data.users.find((user: User) => user.id === option.id);
				if (user) {
					const author = { user: user, position: index };
					zenoClient.updateReportAuthor(data.report.id, author);
					finalList.push(author);
				}
				// Author correct, keep it
			} else {
				finalList.push(authors[index]);
			}
		});
		// Remove authors that are not in the list anymore
		authors.forEach((author) => {
			if (!finalList.find((finalAuthor) => finalAuthor.user.id === author.user.id)) {
				zenoClient.deleteReportAuthor(data.report.id, author);
			}
		});
		authors = finalList.sort((a, b) => a.position - b.position);
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
			<div class="mt-4 flex {!data.report.editor ? 'flex-wrap' : ''} items-center gap-2 gap-x-4">
				<p class="text-lg text-grey-dark">
					Author{authors.length > 1 ? 's' : ''}:
				</p>
				{#if data.report.editor}
					<MultiSelect
						bind:selected={authorsSelected}
						options={authorOptions}
						key={JSON.stringify}
						liSelectedClass="!bg-primary-light ![&>svg]:fill-primary"
						ulSelectedClass="!overflow-x-auto !w-full"
						outerDivClass="!w-full !border-grey-light !py-1 !bg-white"
						liActiveOptionClass="!bg-primary-light"
					>
						<p style="text-wrap: pretty;" slot="selected" let:option>{option.label}</p>
					</MultiSelect>
				{:else}
					{#each authors as author}
						<div class="flex w-fit shrink-0 items-center rounded">
							<Icon class="mr-1 h-6 w-6" tag="svg" viewBox="0 0 24 24">
								<path class="fill-primary" d={mdiAccountCircleOutline} />
							</Icon>
							<p>{author.user.displayName}</p>
						</div>
					{/each}
				{/if}
			</div>

			<div class="mt-2 flex w-full flex-wrap items-center gap-2">
				<p class="mr-2 text-lg text-grey-dark">Linked Projects:</p>
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
					{#each data.projects as project}
						<button
							class="flex w-fit items-center rounded bg-primary-light px-2 py-1 transition hover:bg-primary-mid"
							on:click={() => goto(`/project/${project.uuid}/${encodeURIComponent(project.name)}`)}
						>
							<img src="/zeno-logo-small.svg" alt="Zeno logo" class="mr-1" />
							<p class="mr-1">{project.name}</p>
						</button>
					{/each}
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
				{#if !data.report.editor}
					<div class="relative mt-10 w-full rounded bg-primary p-5">
						<h4 class="text-xl text-white">Enjoyed this report? You can make one too!</h4>
						<p class="mt-2 text-white">
							Error analysis, chart authoring, shareable reports, and more with <b>Zeno</b>.
						</p>
						<div class="mt-6">
							<Button class="bg-white text-white" variant="outlined" href="https://zenoml.com">
								Learn more
							</Button>
							<Button
								class="ml-4 bg-white text-white"
								variant="outlined"
								href="https://zenoml.com/docs/intro"
							>
								Get started
							</Button>
						</div>
						<div class="absolute right-0 top-0 hidden sm:inline">
							<svg
								width="300"
								height="150"
								viewBox="0 0 862 380"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M861.702 424.838L436.864 424.838L436.864 0.000147393L650.895 214.031L861.702 424.838Z"
									fill="#9F55CD"
								>
									<animate
										attributeName="opacity"
										values=".6;1;.6"
										dur="5s"
										repeatCount="indefinite"
									/>
								</path>
								<path
									d="M417.842 426.106L205.423 213.687L417.842 1.26808L417.842 426.106Z"
									fill="#9F55CD"
									fill-opacity="0.8"
								>
									<animate
										attributeName="opacity"
										values=".8;.5;.8"
										dur="5s"
										repeatCount="indefinite"
									/>
								</path>
								<path
									d="M392.478 426.106L193.375 426.106L193.375 227.003L392.478 426.106Z"
									fill="#9F55CD"
									fill-opacity="0.6"
								>
									<animate
										attributeName="opacity"
										values=".4;.8;.4"
										dur="5s"
										repeatCount="indefinite"
									/>
								</path>
								<path
									d="M175.776 425.95L85.1012 335.276L176.255 244.122L175.776 425.95Z"
									fill="#9F55CD"
									fill-opacity="0.5"
								>
									<animate
										attributeName="opacity"
										values=".6;.2;.6"
										dur="5s"
										repeatCount="indefinite"
									/>
								</path>
								<path
									d="M8.92166e-05 417.575L68.7054 348.87L143.13 423.294L8.92166e-05 417.575Z"
									fill="#9F55CD"
									fill-opacity="0.5"
								>
									<animate
										attributeName="opacity"
										values=".2;.4;.2"
										dur="5s"
										repeatCount="indefinite"
									/>
								</path>
							</svg>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
