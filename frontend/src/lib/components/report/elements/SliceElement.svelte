<script lang="ts">
	import { goto } from '$app/navigation';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import type { ViewSchema } from '$lib/instance-views/schema';
	import type { URLParams } from '$lib/util/util';
	import type {
		ReportElement,
		SliceElementOptions,
		SliceElementSpec,
		SliceTableRequest,
		ZenoService
	} from '$lib/zenoapi';
	import { mdiChevronLeft, mdiChevronRight } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/';
	import { getContext } from 'svelte';

	export let element: ReportElement;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let sliceElementSpec: SliceElementSpec | undefined;
	let sliceElementOptions: SliceElementOptions | undefined;
	let table: Record<string, string | number | boolean>[] | undefined = [];
	let page = 0;

	$: updateSliceElementSpec(element.data as string);
	$: viewSchema = JSON.parse(sliceElementOptions?.project.view || '{}') as ViewSchema;
	$: instancesPerPage = viewSchema.size && viewSchema.size === 'large' ? 1 : 2;

	$: if (sliceElementSpec && sliceElementOptions) {
		zenoClient
			.getSliceTable({
				sliceId: sliceElementSpec.sliceId,
				model: sliceElementSpec.systemName,
				offset: page * instancesPerPage,
				limit: instancesPerPage
			} as SliceTableRequest)
			.then((r) => (table = JSON.parse(r)));
	}

	function updateSliceElementSpec(data: string) {
		page = 0;
		try {
			sliceElementSpec = JSON.parse(data) as SliceElementSpec;
			zenoClient
				.getSliceElementOptions(sliceElementSpec)
				.then((r) => (sliceElementOptions = r))
				.catch(() => (sliceElementSpec = undefined));
		} catch {
			sliceElementSpec = undefined;
		}
	}

	function encodeParams() {
		const params = {
			model: sliceElementSpec?.systemName,
			metric: undefined,
			comparisonModel: undefined,
			comparisonColumn: undefined,
			compareSort: undefined,
			metricRange: undefined,
			selections: { slices: [sliceElementSpec?.sliceId], tags: [], metadata: {} }
		} as URLParams;
		return `?params=${btoa(JSON.stringify(params))}`;
	}
</script>

{#if sliceElementOptions !== undefined && sliceElementSpec && table}
	<div class="w-full">
		<div class="mb-2 flex items-center">
			<h3 class="text-lg">
				Slice <span class="font-semibold">{sliceElementOptions.sliceName} </span>
				{#if sliceElementSpec.systemName}
					model
					<span class="font-semibold">{sliceElementSpec.systemName}</span>
				{/if}
			</h3>
			<Button
				variant="outlined"
				class="ml-4"
				on:click={() =>
					goto(
						`/project/${sliceElementOptions?.project.uuid}/${encodeURIComponent(
							sliceElementOptions?.project.name || ''
						)}/explore` + encodeParams()
					)}>Explore</Button
			>
			<p class="ml-auto">
				{page * instancesPerPage + 1} - {Math.min(
					page * instancesPerPage + instancesPerPage,
					sliceElementOptions.sliceSize
				)} of {sliceElementOptions.sliceSize}
			</p>
		</div>
		<div class="flex w-full items-stretch justify-between">
			<button
				class="mr-2 hover:bg-yellowish-light {page === 0
					? 'bg-yellowish-light'
					: ''}  flex items-center"
				disabled={page === 0}
				on:click={() => page--}
			>
				<div class="h-6 w-6 align-middle">
					<Icon tag="svg" viewBox="0 0 24 24">
						<path fill={page === 0 ? 'grey' : 'black'} d={mdiChevronLeft} />
					</Icon>
				</div>
			</button>
			<div class="flex h-full w-full flex-wrap content-start overflow-x-auto">
				{#if sliceElementOptions.idColumn !== undefined && table.length > 0 && table[0][sliceElementOptions.idColumn] !== undefined}
					{#each table as inst (inst[sliceElementOptions.idColumn])}
						<div class="m-auto mt-0 {instancesPerPage === 1 ? 'w-full' : 'w-1/2'} px-1">
							<InstanceView
								view={sliceElementOptions.project.view}
								idColumn={sliceElementOptions.idColumn}
								dataColumn={sliceElementOptions.dataColumn}
								systemColumn={sliceElementOptions.systemColumn}
								labelColumn={sliceElementOptions.labelColumn}
								entry={inst}
							/>
						</div>
					{/each}
				{/if}
			</div>
			<button
				class="flex items-center hover:bg-yellowish-light
				{page * instancesPerPage + instancesPerPage >= sliceElementOptions.sliceSize
					? 'bg-yellowish-light'
					: ''}"
				disabled={page * instancesPerPage + instancesPerPage >= sliceElementOptions.sliceSize}
				on:click={() => page++}
			>
				<div class="h-6 w-6">
					<Icon tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiChevronRight} />
					</Icon>
				</div>
			</button>
		</div>
	</div>
{:else}
	<p class="ml-4 mt-4 font-semibold text-error">Slice does not exist anymore.</p>
{/if}
