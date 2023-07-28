<script lang="ts">
	import { comparisonModel, model, projectConfig, slices } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { updateModelDependentSlices } from '$lib/util/util';
	import { ZenoService, type Slice } from '$lib/zenoapi';
	import { mdiCheckCircle, mdiPlus } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import SliceDetails from '../../general/SliceDetails.svelte';

	export let slice: Slice;
	export let metric: string;
	export let size: number;

	let newSliceName = '';
	let showSliceName = false;
	let created = false;
	let input: Textfield;

	$: if (showSliceName && input) {
		input.getElement().focus();
	}
	$: validSlice =
		newSliceName && $slices.find((sli) => sli.sliceName === newSliceName) === undefined;

	/** Save a generated slice to the slice drawer **/
	function addSlice() {
		slice.sliceName = newSliceName;
		if ($projectConfig !== undefined) {
			ZenoService.addSlice($projectConfig.uuid, slice).then(() => {
				ZenoService.getSlices($projectConfig ? $projectConfig.uuid : '').then((fetchedSlices) => {
					slices.set(fetchedSlices);
					$model !== undefined && updateModelDependentSlices('model A', $model, $slices);
					$comparisonModel !== undefined &&
						updateModelDependentSlices('model B', $comparisonModel, $slices);
					showSliceName = false;
					created = true;
				});
			});
		}
	}

	/** Remove a generated slice from the slice drawer **/
	function removeSlice() {
		ZenoService.deleteSlice(slice).then(() => {
			if ($projectConfig) {
				ZenoService.getSlices($projectConfig.uuid).then((fetchedSlices) => {
					slices.set(fetchedSlices);
					created = false;
				});
			}
		});
	}

	/** Define keyboard actions **/
	function submit(e: KeyboardEvent) {
		e.stopPropagation();
		if (validSlice && e.key === 'Enter') {
			addSlice();
		}
		if (showSliceName && e.key === 'Escape') {
			showSliceName = false;
		}
	}
</script>

<svelte:window on:keydown={submit} />

<div class="ml-5 flex mt-2.5 mb-2.5 items-center justify-between">
	<span style="display: inline-block;">
		<SliceDetails predicateGroup={slice.filterPredicates} />
	</span>
	<div style="display: flex; align-items: center;">
		<span style="margin-right: 10px; margin-left: 10px">
			{metric}
		</span>
		<span class="italic text-grey-dark mr-2.5">
			({size})
		</span>
		{#if created}
			<IconButton on:click={() => removeSlice()}>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="#6a1b9a" d={mdiCheckCircle} />
				</Icon>
			</IconButton>
		{:else}
			<IconButton
				on:click={() => {
					showSliceName = true;
				}}
			>
				<Icon tag="svg" viewBox="0 0 24 24">
					<path fill="#6a1b9a" d={mdiPlus} />
				</Icon>
			</IconButton>
		{/if}
	</div>
	{#if showSliceName}
		<div id="right-8 absolute" use:clickOutside={() => (showSliceName = false)} on:keydown={submit}>
			<Paper elevation={7}>
				<Content style="display:flex; flex-direction:column">
					<Textfield bind:value={newSliceName} label="Slice Name" bind:this={input} />
					<div class="mt-2.5">
						<Button
							style="margin-left: 10px;"
							variant="outlined"
							on:click={() => (showSliceName = false)}
						>
							Cancel
						</Button>
						<Button
							style="margin-left: 5px;"
							variant="outlined"
							disabled={!validSlice}
							on:click={() => addSlice()}
						>
							{'Create'}
						</Button>
					</div>
				</Content>
			</Paper>
		</div>
	{/if}
</div>
