<script lang="ts">
	import { folders, project } from '$lib/stores';
	import type { Folder, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let folderToEdit: Folder | undefined = undefined;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let folderName = folderToEdit ? folderToEdit.name : '';
	let input: Textfield;

	$: invalidName = folderName.length === 0;

	$: if (input) {
		input.getElement().focus();
	}

	function editFolder() {
		if (folderToEdit) {
			zenoClient
				.updateFolder($project.uuid, {
					...folderToEdit,
					name: folderName
				})
				.then(() => {
					folders.update((f) => {
						const index = f.findIndex((f) => f.id === folderToEdit?.id);
						if (index !== -1 && folderToEdit) {
							f[index] = { ...folderToEdit, name: folderName };
						}
						return f;
					});
				});
		}
		dispatch('close');
	}

	/** Create a folder using the folderName variable **/
	function createFolder() {
		zenoClient.addFolder($project.uuid, folderName).then((res) => {
			folders.update((f) => [
				...f,
				{
					id: res,
					name: folderName
				}
			]);
		});
		dispatch('close');
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter' && !invalidName) {
			createFolder();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<Popup on:close>
	<Content class="flex items-end">
		<Textfield bind:value={folderName} label="Folder Name" bind:this={input} />
		<Button class="ml-4" variant="outlined" on:click={() => dispatch('close')}>Cancel</Button>
		<Button
			class="ml-2"
			variant="outlined"
			disabled={invalidName}
			on:click={() => (folderToEdit ? editFolder() : createFolder())}
		>
			{folderToEdit ? 'Update' : 'Create'}
		</Button>
	</Content>
	{#if invalidName && folderName.length > 0}
		<p style:margin-right="10px" style:color="red">folder already exists</p>
	{/if}
</Popup>
