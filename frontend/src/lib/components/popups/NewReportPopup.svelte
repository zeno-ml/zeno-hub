<script lang="ts">
	import { goto } from '$app/navigation';
	import type { ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let user: string;
	export let showNewReport: boolean;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let reportName = '';
	let input: Textfield;

	// TODO: endpoint to check report name
	$: invalidName = reportName.match(/[/]/g) !== null;
	$: if (input) {
		input.getElement().focus();
	}

	function addReport() {
		showNewReport = false;
		zenoClient
			.addReport(reportName)
			.then(() => goto(`/report/${user}/${encodeURIComponent(reportName)}`));
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			if (!invalidName && reportName.length > 0) addReport();
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; align-items: center;">
		<Textfield bind:value={reportName} label="Report Name" />
		<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}>
			Cancel
		</Button>
		<Button
			style="margin-left: 5px;"
			variant="outlined"
			disabled={invalidName}
			on:click={addReport}
		>
			Create
		</Button>
	</Content>
	{#if invalidName && reportName.length > 0}
		<p class="mt-2 text-primary">
			{#if reportName.match(/[/]/g) !== null}
				A report name cannot contain a "/".
			{:else}
				report already exists
			{/if}
		</p>
	{/if}
</Popup>
