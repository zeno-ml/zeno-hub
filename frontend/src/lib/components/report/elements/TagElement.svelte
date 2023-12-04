<script lang="ts">
	import { goto } from '$app/navigation';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import type { URLParams } from '$lib/util/util';
	import type {
		ReportElement,
		TagElementOptions,
		TagElementSpec,
		TagTableRequest,
		ZenoService
	} from '$lib/zenoapi';
	import { mdiChevronLeft, mdiChevronRight } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/';
	import { getContext } from 'svelte';

	export let element: ReportElement;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let tagElementSpec: TagElementSpec | undefined;
	let tagElementOptions: TagElementOptions | undefined;
	let table: Record<string, string | number | boolean>[] | undefined;
	let page = 0;

	$: updateTagElementSpec(element.data as string);

	$: if (tagElementSpec && tagElementOptions) {
		zenoClient
			.getTagTable({
				tagId: tagElementSpec.tagId,
				model: tagElementSpec.systemName,
				offset: page * 2,
				limit: 2
			} as TagTableRequest)
			.then((r) => (table = JSON.parse(r)));
	}

	function updateTagElementSpec(data: string) {
		page = 0;
		try {
			tagElementSpec = JSON.parse(data) as TagElementSpec;
			zenoClient.getTagElementOptions(tagElementSpec).then((r) => (tagElementOptions = r));
		} catch {
			tagElementSpec = undefined;
		}
	}

	function encodeParams() {
		const params = {
			model: tagElementSpec?.systemName,
			metric: undefined,
			comparisonModel: undefined,
			comparisonColumn: undefined,
			compareSort: undefined,
			metricRange: undefined,
			selections: { slices: [], tags: [tagElementSpec?.tagId], metadata: {} }
		} as URLParams;
		return `?params=${btoa(JSON.stringify(params))}`;
	}
</script>

{#if tagElementOptions !== undefined && tagElementSpec && table}
	<div class="w-full">
		<div class="mb-2 flex items-center">
			<h3 class="text-lg">
				Tag <span class="font-semibold">{tagElementOptions.tagName} </span>
				{#if tagElementSpec.systemName}
					model
					<span class="font-semibold">{tagElementSpec.systemName}</span>
				{/if}
			</h3>
			<Button
				variant="outlined"
				class="ml-4"
				on:click={() =>
					goto(
						`/project/${tagElementOptions?.project.ownerName}/${tagElementOptions?.project.name}/explore` +
							encodeParams()
					)}>Explore</Button
			>
			<p class="ml-auto">
				{page * 2 + 1} - {Math.min(page * 2 + 2, tagElementOptions.tagSize)} of {tagElementOptions.tagSize}
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
					<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
						<path fill={page === 0 ? 'grey' : 'black'} d={mdiChevronLeft} />
					</Icon>
				</div>
			</button>
			<div class="flex h-full w-full flex-wrap content-start overflow-x-auto">
				{#if tagElementOptions.idColumn !== undefined && table.length > 0 && table[0][tagElementOptions.idColumn] !== undefined}
					{#each table as inst (inst[tagElementOptions.idColumn])}
						<div class="m-auto mt-0 w-1/2 px-1">
							<InstanceView
								view={tagElementOptions.project.view}
								dataColumn={tagElementOptions.dataColumn}
								systemColumn={tagElementOptions.systemColumn}
								labelColumn={tagElementOptions.labelColumn}
								entry={inst}
							/>
						</div>
					{/each}
				{/if}
			</div>
			<button
				class="flex items-center hover:bg-yellowish-light
				{page * 2 + 2 >= tagElementOptions.tagSize ? 'bg-yellowish-light' : ''}"
				disabled={page * 2 + 2 >= tagElementOptions.tagSize}
				on:click={() => page++}
			>
				<div class="h-6 w-6">
					<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiChevronRight} />
					</Icon>
				</div>
			</button>
		</div>
	</div>
{/if}
