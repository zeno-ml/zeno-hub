<script lang="ts">
	import { goto } from '$app/navigation';
	import { showNewReport } from '$lib/stores';
	import type { Report, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let user: string;
	export let reports: Report[];

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let reportName = '';
	let input: Textfield;

	$: invalidName = reports.filter((rep) => rep.name === reportName).length > 0;
	$: if (input) {
		input.getElement().focus();
	}

	function addReport() {
		showNewReport.set(false);
		zenoClient.addReport(reportName).then(() => goto(`/report/${user}/${reportName}`));
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
		<p style:margin-right="10px" style:color="red">report already exists</p>
	{/if}
</Popup>
