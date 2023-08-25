<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import Report from '$lib/components/report/Report.svelte';
	import { ZenoService } from '$lib/zenoapi';
	import { mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';

	export let data;

	$: ownReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName === data.user?.name);
	$: sharedReports =
		data.user === null ? [] : data.reports.filter((rep) => rep.ownerName !== data.user?.name);
	$: publicReports = data.publicReports.filter(
		(rep) =>
			ownReports.find((own) => own.id === rep.id) === undefined &&
			sharedReports.find((shared) => shared.id === rep.id) === undefined
	);
</script>

<div class="flex flex-col m-2">
	{#if data.user}
		<h1 class="text-lg">Your reports</h1>
		<div class="mb-4 flex flex-wrap items-start">
			{#each ownReports as report}
				<Report {report} deletable />
			{/each}
			<button
				class="flex flex-col justify-around items-center border-2 border-grey-lighter rounded-lg m-2 px-2.5 w-48 h-24 hover:bg-primary-light"
				on:click={() => {
					ZenoService.addReport('new_report').then(() => {
						invalidateAll();
					});
				}}
			>
				<div class="w-6 h-6">
					<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiPlus} />
					</Icon>
				</div>
			</button>
		</div>
		{#if sharedReports.length > 0}
			<h1 class="text-lg">Shared reports</h1>
			<div class="mb-4 flex flex-wrap items-start">
				{#each sharedReports as report}
					<Report {report} />
				{/each}
			</div>
		{/if}
	{/if}
	{#if publicReports.length > 0}
		<h1 class="text-lg">Public reports</h1>
		<div class="mb-4 flex flex-wrap items-start">
			{#each publicReports as report}
				<Report {report} />
			{/each}
		</div>
	{/if}
</div>
