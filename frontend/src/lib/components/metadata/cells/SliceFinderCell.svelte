<script lang="ts">
	import { project, slices } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import type { Slice, ZenoService } from '$lib/zenoapi';
	import { mdiCheckCircle, mdiPlus } from '@mdi/js';
	import Button from '@smui/button';
	import IconButton, { Icon } from '@smui/icon-button';
	import Paper, { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { getContext } from 'svelte';
	import SliceDetails from '../../general/SliceDetails.svelte';

	export let slice: Slice;
	export let metric: string;
	export let size: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

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
		zenoClient.addSlice($project.uuid, slice).then((res) => {
			slices.update((s) => [...s, { ...slice, id: res }]);
			showSliceName = false;
			created = true;
		});
	}

	/** Remove a generated slice from the slice drawer **/
	function removeSlice() {
		zenoClient.deleteSlice($project.uuid, slice.id).then(() => {
			slices.update((s) => s.filter((sli) => sli.id !== slice.id));
			created = false;
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

<div class="mb-2.5 ml-5 mt-2.5 flex items-center justify-between">
	<span class="inline-block">
		<SliceDetails predicateGroup={slice.filterPredicates} />
	</span>
	<div class="flex items-center">
		<span style="margin-right: 10px; margin-left: 10px">
			{metric}
		</span>
		<span class="mr-2.5 italic text-grey-dark">
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
		<button
			id="right-8 absolute"
			use:clickOutside={() => (showSliceName = false)}
			on:keydown={submit}
		>
			<Paper elevation={7}>
				<Content class="flex flex-col">
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
		</button>
	{/if}
</div>
