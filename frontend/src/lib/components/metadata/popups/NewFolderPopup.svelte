<script lang="ts">
	import { currentProject, folderToEdit, folders, showNewFolder } from '$lib/stores';
	import { clickOutside } from '$lib/util/clickOutside';
	import { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import Paper, { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';

	let folderName = '';
	let input: Textfield;

	$: invalidName = folderName.length === 0;

	$: if ($showNewFolder && input) {
		input.getElement().focus();
	}

	$: if ($folderToEdit) {
		folderName = $folderToEdit.name;
	}

	function editFolder() {
		if ($folderToEdit && $currentProject) {
			ZenoService.updateFolder($currentProject.uuid, {
				...$folderToEdit,
				name: folderName
			}).then(() => {
				if ($currentProject) {
					ZenoService.getFolders($currentProject.uuid).then((fetchedFolders) =>
						folders.set(fetchedFolders)
					);
				}
			});
		}
		showNewFolder.set(false);
	}

	/** Create a folder using the folderName variable **/
	function createFolder() {
		if ($currentProject) {
			ZenoService.addFolder($currentProject.uuid, folderName).then(() => {
				if ($currentProject) {
					ZenoService.getFolders($currentProject.uuid).then((fetchedFolders) =>
						folders.set(fetchedFolders)
					);
				}
			});
		}
		showNewFolder.set(false);
	}

	/** Define keyboard action **/
	function submit(e) {
		if ($showNewFolder && e.key === 'Escape') {
			showNewFolder.set(false);
		}
		if ($showNewFolder && e.key === 'Enter' && !invalidName) {
			createFolder();
		}
	}
</script>

<svelte:window on:keydown={submit} />

<div id="paper-container" use:clickOutside on:clickOutside={() => showNewFolder.set(false)}>
	<Paper elevation={7}>
		<Content style="display: flex; align-items: center;">
			<Textfield bind:value={folderName} label="Folder Name" bind:this={input} />
			<Button
				style="margin-left: 10px;"
				variant="outlined"
				on:click={() => showNewFolder.set(false)}
			>
				Cancel
			</Button>
			<Button
				style="margin-left: 5px;"
				variant="outlined"
				disabled={invalidName}
				on:click={() => ($folderToEdit ? editFolder() : createFolder())}
			>
				{$folderToEdit ? 'Update' : 'Create'}
			</Button>
		</Content>
		{#if invalidName && folderName.length > 0}
			<p style:margin-right="10px" style:color="red">folder already exists</p>
		{/if}
	</Paper>
</div>

<style>
	#paper-container {
		position: fixed;
		left: 440px;
		top: 70px;
		z-index: 20;
	}
</style>
