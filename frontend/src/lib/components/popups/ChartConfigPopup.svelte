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

	function resetChartConfig() {
		config = oldConfig;
		dispatch('close');
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			resetChartConfig();
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content
		style="display: flex; flex-direction: column; width: 400px; max-height: 80vh; overflow-y: scroll"
	>
		<h2 class="mb-4 text-xl">Chart Configuration</h2>
		<div>
			<Textfield bind:value={config.fontSize} label="Font Size" class="mb-4 w-full" type="number" />
		</div>
		<div class="flex items-center self-end">
			<Button style="margin-left: 10px;" variant="outlined" on:click={resetChartConfig}
				>Cancel</Button
			>
			<Button style="margin-left: 5px;" variant="outlined" on:click={updateChartConfig}
				>{'Update'}</Button
			>
		</div>
	</Content>
</Popup>
