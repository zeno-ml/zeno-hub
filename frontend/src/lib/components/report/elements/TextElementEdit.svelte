<script lang="ts">
	import type { ReportElement, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';

	export let element: ReportElement;
	export let reportId: number;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let timer: ReturnType<typeof setTimeout>;

	function updateData() {
		clearTimeout(timer);
		timer = setTimeout(() => {
			zenoClient.updateReportElement(reportId, element);
		}, 1000);
	}
</script>

<textarea
	class="h-full min-h-[150px] w-full rounded border border-grey-light p-2"
	on:input={updateData}
	bind:value={element.data}
/>
