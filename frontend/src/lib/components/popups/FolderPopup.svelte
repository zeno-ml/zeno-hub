<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { folders, project } from '$lib/stores';
	import { ZenoService, type Folder } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher } from 'svelte';
	import Popup from './Popup.svelte';

	export let folderToEdit: Folder | undefined = undefined;

	let dispatch = createEventDispatcher();

	let folderName = folderToEdit ? folderToEdit.name : '';
	let input: Textfield;

	$: invalidName = folderName.length === 0;

	$: if (input) {
		input.getElement().focus();
	}

	function editFolder() {
		if (folderToEdit && $project) {
			ZenoService.updateFolder($project.uuid, {
				...folderToEdit,
				name: folderName
			}).then(() => {
				invalidate('app:state');
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
		if ($project) {
			ZenoService.addFolder($project.uuid, folderName).then((res) => {
				invalidate('app:state');
				folders.update((f) => [
					...f,
					{
						id: res,
						name: folderName
					}
				]);
			});
		}
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
	<Content style="display: flex; align-items: center;">
		<Textfield bind:value={folderName} label="Folder Name" bind:this={input} />
		<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}>
			Cancel
		</Button>
		<Button
			style="margin-left: 5px;"
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
