<script lang="ts">
	import { columns, project, selectionPredicates, selections, slices } from '$lib/stores';
	import { isPredicateGroup } from '$lib/util/typeCheck';
	import {
		Join,
		Operation,
		ZenoService,
		type FilterPredicate,
		type FilterPredicateGroup,
		type Slice
	} from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher } from 'svelte';
	import FilterGroupEntry from './FilterGroupEntry.svelte';
	import Popup from './Popup.svelte';

	export let sliceToEdit: Slice | undefined = undefined;

	const dispatch = createEventDispatcher();

	let sliceName = '';
	let folderId: number | undefined;
	let predicateGroup: FilterPredicateGroup = { predicates: [], join: Join._ };
	let nameInput: Textfield;

	// Track original settings when editing.
	let originalName = '';
	let originalPredicates;

	$: isValidPredicates = checkValidPredicates(predicateGroup.predicates);
	$: if (nameInput) {
		nameInput.getElement().focus();
	}
	// Declare this way instead of subscribe to avoid mis-tracking on $sliceToEdit.
	$: updatePredicates();

	// check if predicates are valid (not empty)
	function checkValidPredicates(preds: (FilterPredicateGroup | FilterPredicate)[]): boolean {
		let valid = preds.length > 0;
		preds.forEach((p, i) => {
			if (i !== 0 && p.join === Join._) {
				valid = false;
			} else {
				if (isPredicateGroup(p)) {
					valid = checkValidPredicates(p.predicates);
				} else {
					if (
						p.column === null ||
						p.operation === undefined ||
						p.value === '' ||
						p.value === null
					) {
						valid = false;
					}
				}
			}
		});
		return valid;
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

		if (sliceToEdit && $project) {
			ZenoService.updateSlice($project.uuid, {
				id: sliceToEdit.id,
				sliceName,
				filterPredicates: predicateGroup,
				folderId: folderId
			});
		} else {
			ZenoService.addSlice($project ? $project.uuid : '', {
				id: 0,
				sliceName,
				filterPredicates: predicateGroup,
				folderId: folderId
			}).then(() => {
				ZenoService.getSlices($project ? $project.uuid : '').then((fetchedSlices) => {
					slices.set(fetchedSlices);
					selections.update(() => ({
						slices: [],
						metadata: {},
						tags: []
					}));
					dispatch('close');
				});
			});
		}
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			saveSlice();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<Popup on:close>
	<Content>
		<Textfield bind:value={sliceName} label="Slice Name" bind:this={nameInput} />
		<FilterGroupEntry index={-1} deletePredicate={() => deletePredicate(-1)} bind:predicateGroup />
		<div class="flex items-center flex-row-reverse">
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
			<Button style="margin-right: 10px" variant="outlined" on:click={() => dispatch('close')}>
				cancel
			</Button>
			{#if (!sliceToEdit && $slices.some((slice) => slice.sliceName === sliceName)) || (sliceToEdit && originalName !== sliceName && $slices.some((slice) => slice.sliceName === sliceName))}
				<p style:margin-right="10px" style:color="red">slice already exists</p>
			{/if}
		</div>
	</Content>
</Popup>
