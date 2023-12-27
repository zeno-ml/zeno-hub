<script lang="ts">
	import Header from '$lib/components/general/Header.svelte';
	import Confirm from '$lib/components/popups/Confirm.svelte';
	import ReportPopup from '$lib/components/popups/ReportPopup.svelte';
	import AddElementButton from '$lib/components/report/AddElementButton.svelte';
	import Banner from '$lib/components/report/Banner.svelte';
	import ElementContainer from '$lib/components/report/ElementContainer.svelte';
	import LinkedProjects from '$lib/components/report/LinkedProjects.svelte';
	import { ReportElementType, ZenoService, type Author, type User } from '$lib/zenoapi';
	import { mdiAccountCircleOutline } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { getContext } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';

	export let data;

	let reportEdit = false;
	let elements = data.reportElements.sort((a, b) => a.position - b.position);
	let authors: Author[] = data.authors.sort((a: Author, b: Author) => a.position - b.position);
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
						<p class="text-pretty" slot="selected" let:option>{option.label}</p>
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

			<LinkedProjects linkedProjects={data.projects} report={data.report} />

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
					<Banner />
				{/if}
			</div>
		</div>
	</div>
</div>
