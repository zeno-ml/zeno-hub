<script lang="ts">
	import type { ChartConfig, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let config: ChartConfig;
	export let chartId: number | null = null;

	const oldConfig = { ...config };
	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	function updateChartConfig() {
		zenoClient.updateChartConfig(config, chartId).then(() => {
			dispatch('close');
		});
	}

	function undoChartConfig() {
		config = oldConfig;
		dispatch('close');
	}

	function resetChartConfig() {
		zenoClient.deleteChartConfig(config.projectUuid, chartId).then(() => {
			zenoClient.getChartConfig(config.projectUuid, chartId).then((fetchedConfig) => {
				config = fetchedConfig;
			});
		});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			undoChartConfig();
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content class="flex max-h-[80vh] w-[600px] flex-col overflow-y-auto">
		<h2 class="mb-4 text-xl">Chart Configuration</h2>
		<div>
			<Textfield bind:value={config.fontSize} label="Font Size" class="mb-4 w-full" type="number" />
		</div>
		<div class="flex items-center">
			<Button on:click={resetChartConfig}
				>Reset to {chartId === null ? 'Default' : 'Project Settings'}</Button
			>
			<Button class="ml-auto" variant="outlined" on:click={undoChartConfig}>Cancel</Button>
			<Button class="ml-2" variant="outlined" on:click={updateChartConfig}>Update</Button>
		</div>
	</Content>
</Popup>
