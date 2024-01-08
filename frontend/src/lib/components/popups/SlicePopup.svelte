<script lang="ts">
	import { columns, folders, project, selectionPredicates, selections, slices } from '$lib/stores';
	import { isPredicateGroup } from '$lib/util/typeCheck';
	import {
		Join,
		MetadataType,
		Operation,
		ZenoColumnType,
		type FilterPredicate,
		type FilterPredicateGroup,
		type Slice,
		type ZenoService
	} from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import FilterGroupEntry from './FilterGroupEntry.svelte';
	import Popup from './Popup.svelte';

	export let sliceToEdit: Slice | undefined = undefined;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let sliceName = '';
	let folderId: number | undefined;
	let predicateGroup: FilterPredicateGroup = { predicates: [], join: Join._ };
	let nameInput: Textfield;
	let error: string | undefined = undefined;

	// Track original settings when editing.
	let originalName = '';
	let originalPredicates;

	$: isValidPredicates = checkValidPredicates(predicateGroup.predicates);
	$: if (nameInput) {
		nameInput.getElement().focus();
	}
	// Declare this way instead of subscribe to avoid mis-tracking on $sliceToEdit.
	$: updatePredicates();
	$: {
		predicateGroup;
		error = undefined;
	}

	// check if predicates are valid (not empty)
	function checkValidPredicates(preds: (FilterPredicateGroup | FilterPredicate)[]): boolean {
		for (const [index, predicate] of preds.entries()) {
			if (index !== 0 && predicate.join === Join._) {
				return false;
			} else {
				if (isPredicateGroup(predicate)) {
					if (!checkValidPredicates(predicate.predicates)) return false;
				} else {
					if (
						predicate.column === null ||
						predicate.operation === undefined ||
						predicate.value === '' ||
						predicate.value === null
					) {
						return false;
					}
					if (
						predicate.operation === Operation.REGEX ||
						predicate.operation === Operation.NOT_REGEX
					) {
						try {
							new RegExp(String(predicate.value));
						} catch (e) {
							return false;
						}
					}
				}
			}
		}
		return preds.length > 0;
	}

	function updatePredicates() {
		predicateGroup = { predicates: [], join: Join._ };

		if (sliceToEdit) {
			sliceName = sliceToEdit.sliceName;
			predicateGroup = sliceToEdit.filterPredicates;
			folderId = sliceToEdit.folderId === null ? undefined : sliceToEdit.folderId;
			originalName = sliceName;
			// deep copy of predicate group to avoid sharing nested objects
			originalPredicates = JSON.parse(JSON.stringify(predicateGroup));

			// revert to original settings when close the slice popup w/ invalid predicates
			if (!isValidPredicates) {
				predicateGroup = originalPredicates;
			}
			return;
		}

		if ($selectionPredicates !== undefined) {
			// prefill slice creation popup with selection bar filter predicates
			predicateGroup = JSON.parse(JSON.stringify($selectionPredicates));
		}

		// If no predicates, add an empty one.
		if (predicateGroup.predicates.length === 0) {
			predicateGroup.predicates.push({
				column: $columns[0],
				operation: Operation.EQUAL,
				value: '',
				join: Join._
			});
		}
	}

	function deletePredicate(index: number) {
		predicateGroup.predicates.splice(index, 1);
		if (predicateGroup.predicates.length !== 0) {
			predicateGroup.predicates[0].join = Join._;
		}
		predicateGroup = predicateGroup;
	}

	function saveSlice() {
		if (sliceName.length === 0) {
			sliceName = 'Slice ' + $slices.length;
		}

		if (sliceToEdit) {
			zenoClient
				.updateSlice($project.uuid, {
					id: sliceToEdit.id,
					sliceName,
					filterPredicates: predicateGroup,
					folderId: folderId
				})
				.then(() => {
					slices.update((s) => {
						const index = s.findIndex((slice) => slice.id === sliceToEdit?.id);
						s[index] = {
							id: sliceToEdit ? sliceToEdit.id : -1,
							sliceName,
							filterPredicates: predicateGroup,
							folderId: folderId
						};
						return s;
					});
				});
		} else {
			zenoClient
				.addSlice($project.uuid, {
					id: 0,
					sliceName,
					filterPredicates: predicateGroup,
					folderId: folderId
				})
				.then((res) => {
					slices.update((s) => [
						...s,
						{
							id: res,
							sliceName,
							filterPredicates: predicateGroup,
							folderId: folderId
						}
					]);
					selections.update(() => ({
						slices: [],
						metadata: {},
						tags: []
					}));
				});
		}
		dispatch('close');
	}

	function createAllSlices() {
		const predicates = predicateGroup.predicates[0];
		if (Object.hasOwn(predicates, 'column'))
			zenoClient
				.addAllSlices(
					$project.uuid,
					(predicates as FilterPredicate).column,
					sliceName === '' ? undefined : sliceName
				)
				.then(() => {
					zenoClient
						.getFolders($project.uuid)
						.then((fetchedFolders) => folders.set(fetchedFolders));
					zenoClient.getSlices($project.uuid).then((fetchedSlices) => slices.set(fetchedSlices));
					dispatch('close');
				})
				.catch((err) => {
					error = err.body['detail'];
				});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			saveSlice();
		}
	}

	function checkNominalSinglePredicateNoEntry(predicates: FilterPredicateGroup) {
		return (
			!sliceToEdit &&
			predicates.predicates.length === 1 &&
			Object.hasOwn(predicates.predicates[0], 'column') &&
			(predicates.predicates[0] as FilterPredicate).column.dataType === MetadataType.NOMINAL &&
			(predicates.predicates[0] as FilterPredicate).column.columnType !== ZenoColumnType.ID &&
			(predicates.predicates[0] as FilterPredicate).column.columnType !== ZenoColumnType.DATA &&
			(predicates.predicates[0] as FilterPredicate).value === ''
		);
	}
</script>

<svelte:window on:keydown={submit} />

<Popup on:close>
	<Content>
		<Textfield class="mb-2 ml-3" bind:value={sliceName} label="Slice Name" bind:this={nameInput} />
		<FilterGroupEntry index={-1} deletePredicate={() => deletePredicate(-1)} bind:predicateGroup />
		<div class="flex flex-row-reverse items-center">
			{#if checkNominalSinglePredicateNoEntry(predicateGroup)}
				<Button
					variant="outlined"
					on:click={createAllSlices}
					disabled={$slices.some((slice) => slice.sliceName === sliceName)}
				>
					{'Create Slices for all Values'}
				</Button>
			{:else}
				<Button
					variant="outlined"
					on:click={saveSlice}
					disabled={(!sliceToEdit && $slices.some((slice) => slice.sliceName === sliceName)) ||
						(sliceToEdit &&
							originalName !== sliceName &&
							$slices.some((slice) => slice.sliceName === sliceName)) ||
						!isValidPredicates}
				>
					{sliceToEdit ? 'Update Slice' : 'Create Slice'}
				</Button>
			{/if}
			<Button class="mr-4" variant="outlined" on:click={() => dispatch('close')}>cancel</Button>
			{#if (!sliceToEdit && $slices.some((slice) => slice.sliceName === sliceName)) || (sliceToEdit && originalName !== sliceName && $slices.some((slice) => slice.sliceName === sliceName))}
				<p style:margin-right="10px" style:color="red">slice already exists</p>
			{/if}
		</div>
		{#if error}
			<div class="flex flex-row-reverse items-center">
				<p class="mt-2">{error}</p>
			</div>
		{/if}
	</Content>
</Popup>
