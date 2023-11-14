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
	class="h-full w-full rounded border border-grey-light p-2"
	style="min-height: 150px;"
	on:input={updateData}
	bind:value={element.data}
/>
