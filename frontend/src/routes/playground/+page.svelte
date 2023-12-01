<script lang="ts">
	import { page } from '$app/stores';
	import InstanceView from '$lib/instance-views/InstanceView.svelte';
	import { json } from '@codemirror/lang-json';
	import CodeMirror from 'svelte-codemirror-editor';

	import { browser } from '$app/environment';
	import Help from '$lib/components/general/Help.svelte';
	import Error from '$lib/instance-views/Error.svelte';
	import Button from '@smui/button/src/Button.svelte';
	import { samples } from './samples.js';
	import { setURLParameters, type URLParams } from './util.js';

	let sample: string | undefined;

	const searchParams = browser && $page.url.searchParams;
	if (searchParams && searchParams.get('params')) {
		const decodedString = atob(searchParams.get('params') ?? '');
		const urlParams = JSON.parse(decodedString) as URLParams;
		sample = urlParams.sample;
	}

	let spec = sample === undefined ? samples[Object.keys(samples)[0]].spec : samples[sample].spec;
	let currentData =
		sample === undefined ? samples[Object.keys(samples)[0]].data : samples[sample].data;
	let jsonData: Record<string, unknown> | undefined = undefined;
	let errorMessage: string | undefined = undefined;
	let codeHeight: number = 0;

	$: setURLParameters(sample);

	$: try {
		jsonData = JSON.parse(currentData);
		errorMessage = undefined;
	} catch (error) {
		jsonData = undefined;
		errorMessage = error as string;
	}
</script>

<div class="absolute bottom-4 right-4">
	<Help docsLink="https://zenoml.com/docs/views/" />
</div>

<div class="flex h-full w-full flex-col p-4">
	<div class="mb-4 flex h-12 items-center">
		<a href="/" class="shrink-0">
			<img src="/zeno-logo.png" class="h-8" alt="diamond tesselation logo" />
		</a>
		<h1 class="ml-3 text-2xl font-bold">Instance View Playground</h1>
		<div class="ml-auto mr-2">
			<Button variant="raised" href="https://zenoml.com/docs/views/">Read the Docs</Button>
		</div>
	</div>
	<div class="flex w-full items-center pb-4">
		<h2 class="pr-4 text-xl">Standard Views:</h2>
		<div class="flex items-center overflow-x-auto">
			{#each Object.keys(samples) as currentSample}
				<button
					class="mr-2 cursor-pointer whitespace-nowrap rounded-full border border-grey-light p-2 hover:bg-grey-lighter {spec ===
						samples[currentSample].spec && currentData === samples[currentSample].data
						? 'bg-primary-light'
						: 'bg-transparent'}"
					on:click={() => {
						spec = samples[currentSample].spec;
						currentData = samples[currentSample].data;
						sample = currentSample;
					}}>{currentSample}</button
				>
			{/each}
		</div>
	</div>
	<div class="flex h-full min-h-0 w-full">
		<div class="h-full w-1/3 border-r border-grey-light p-2">
			<div class="flex h-full flex-col">
				<h2 class="mb-4 text-xl font-bold">View Specification</h2>
				<div class="min-h-0 grow" bind:clientHeight={codeHeight}>
					<CodeMirror
						bind:value={spec}
						lang={json()}
						styles={{
							'&': {
								height: `${codeHeight}px`
							}
						}}
					/>
				</div>
			</div>
		</div>
		<div class="h-full w-1/3 border-r border-grey-light p-2">
			<div class="flex h-full flex-col">
				<h2 class="mb-4 text-xl font-bold">Data Sample</h2>
				<div class="min-h-0 grow">
					<CodeMirror
						bind:value={currentData}
						lang={json()}
						styles={{
							'&': {
								height: `${codeHeight}px`
							}
						}}
					/>
				</div>
			</div>
		</div>
		<div class="h-full w-1/3 p-2">
			<div class="flex h-full flex-col">
				<h2 class="mb-4 text-xl font-bold">Instance View</h2>
				{#if jsonData === undefined}
					<Error type="Incorrect Data" message={errorMessage} />
				{:else}
					<div class="min-h-0 overflow-y-auto">
						<InstanceView
							view={spec}
							entry={jsonData}
							dataColumn="data"
							labelColumn="label"
							modelColumn="output"
						/>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
