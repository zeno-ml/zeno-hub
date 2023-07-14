<script lang="ts">
	import {
		columns,
		currentProject,
		selectionPredicates,
		selections,
		showNewSlice,
		sliceToEdit,
		slices
	} from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { isPredicateGroup } from '$lib/util/typeCheck';
	import {
		Join,
		Operation,
		ZenoService,
		type FilterPredicate,
		type FilterPredicateGroup
	} from '$lib/zenoapi';
	import Button from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import FilterGroupEntry from './FilterGroupEntry.svelte';

	let sliceName = '';
	let folderId: number | undefined;
	let predicateGroup: FilterPredicateGroup = { predicates: [], join: Join._ };
	let nameInput: Textfield;
	let paperHeight;

	// Track original settings when editing.
	let originalName = '';
	let originalPredicates;

	$: isValidPredicates = checkValidPredicates(predicateGroup.predicates);
	$: if ($showNewSlice && nameInput) {
		nameInput.getElement().focus();
	}
	// Declare this way instead of subscribe to avoid mis-tracking on $sliceToEdit.
	$: $showNewSlice, updatePredicates();

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

		if ($sliceToEdit) {
			sliceName = $sliceToEdit.sliceName;
			predicateGroup = $sliceToEdit.filterPredicates;
			folderId = $sliceToEdit.folderId;
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

		if ($sliceToEdit && $currentProject) {
			ZenoService.updateSlice($currentProject.uuid, {
				id: $sliceToEdit.id,
				sliceName,
				filterPredicates: predicateGroup,
				folderId: folderId
			});
		} else {
			ZenoService.addSlice($currentProject ? $currentProject.uuid : '', {
				id: 0,
				sliceName,
				filterPredicates: predicateGroup,
				folderId: folderId
			}).then(() => {
				ZenoService.getSlices($currentProject ? $currentProject.uuid : '').then((fetchedSlices) => {
					slices.set(fetchedSlices);
					selections.update(() => ({
						slices: [],
						metadata: {},
						tags: []
					}));
					showNewSlice.set(false);
					sliceToEdit.set(undefined);
				});
			});
		}
	}

	function submit(e: KeyboardEvent) {
		if ($showNewSlice && e.key === 'Enter') {
			saveSlice();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<div
	id="paper-container"
	bind:clientHeight={paperHeight}
	use:clickOutside
	on:clickOutside={() => showNewSlice.set(false)}
>
	<Paper
		elevation={7}
		class="paper"
		style="max-height: 75vh; {paperHeight && paperHeight > window.innerHeight * 0.75
			? 'overflow-y: scroll'
			: 'overflow-y: show'}"
	>
		<Content>
			<Textfield bind:value={sliceName} label="Slice Name" bind:this={nameInput} />
			<FilterGroupEntry
				index={-1}
				deletePredicate={() => deletePredicate(-1)}
				bind:predicateGroup
			/>
			<div id="submit">
				<Button
					variant="outlined"
					on:click={saveSlice}
					disabled={(!$sliceToEdit && $slices.some((slice) => slice.sliceName === sliceName)) ||
						($sliceToEdit &&
							originalName !== sliceName &&
							$slices.some((slice) => slice.sliceName === sliceName)) ||
						!isValidPredicates}
				>
					{$sliceToEdit ? 'Update Slice' : 'Create Slice'}
				</Button>
				<Button
					style="margin-right: 10px"
					variant="outlined"
					on:click={() => showNewSlice.set(false)}
				>
					cancel
				</Button>
				{#if (!$sliceToEdit && $slices.some((slice) => slice.sliceName === sliceName)) || ($sliceToEdit && originalName !== sliceName && $slices.some((slice) => slice.sliceName === sliceName))}
					<p style:margin-right="10px" style:color="red">slice already exists</p>
				{/if}
			</div>
		</Content>
	</Paper>
</div>

<style>
	#paper-container {
		position: fixed;
		left: 440px;
		top: 70px;
		z-index: 20;
	}
	#submit {
		display: flex;
		flex-direction: row-reverse;
		align-items: center;
	}
</style>
