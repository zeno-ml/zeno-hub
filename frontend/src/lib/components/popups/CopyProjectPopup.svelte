<script lang="ts">
	import { invalidate } from '$app/navigation';
	import type { Project, User, ZenoService } from '$lib/zenoapi';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let config: Project;
	export let user: User;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let input: Textfield;
	let copyData = true;
	let copySystems = true;
	let copySlices = true;
	let copyCharts = true;
	let step = 1;
	let oldName = config.name;

	$: invalidName =
		config.name.length === 0 ||
		(config.name === oldName && config.ownerName === user.name) ||
		config.name.match(/[/]/g) !== null;
	$: if (input) {
		input.getElement().focus();
	}

	function copyProject() {
		zenoClient
			.copyProject(config.uuid, {
				name: config.name,
				dataUrl: null,
				copyCharts: copyCharts,
				copyData: copyData,
				copySlices: copySlices,
				copySystems: copySystems
			})
			.then(() => {
				invalidate('app:projects');
				step = 2;
			});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			copyProject();
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; flex-direction: column; width: 800px;">
		<h2 class="text-xl mb-4">Copy Project</h2>
		<div class="mb-12 flex flex-col">
			{#if step === 1}
				<div>
					<Textfield
						bind:value={config.name}
						label="Name"
						bind:this={input}
						invalid={invalidName}
					/>
				</div>
				<div>
					<Textfield bind:value={config.dataUrl} label="Data base URL" />
				</div>
				<div class="flex items-center">
					<Checkbox bind:checked={copyData} />
					<span>Copy Data</span>
				</div>
				{#if copyData}
					<div class="flex items-center">
						<Checkbox bind:checked={copySystems} />
						<span>Copy Systems</span>
					</div>
				{/if}
				{#if copyData && copySystems}
					<div class="flex items-center">
						<Checkbox bind:checked={copySlices} />
						<span>Copy Slices</span>
					</div>
				{/if}
				{#if copyData && copySystems && copySlices}
					<div class="flex items-center">
						<Checkbox bind:checked={copyCharts} />
						<span>Copy Charts</span>
					</div>
				{/if}
				<div class="flex items-center self-end">
					<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}
						>Cancel</Button
					>
					<Button
						style="margin-left: 5px;"
						variant="outlined"
						disabled={invalidName}
						on:click={() => copyProject()}>{'Copy'}</Button
					>
				</div>
			{:else}
				<div class="flex mb-6">
					<div class="flex flex-col mr-8">
						<div class="mb-4">
							Your Project has been copied and can be accessed at <a
								href={`/project/${user.name}/${encodeURIComponent(config.name)}`}
								target="_blank"
								class="text-primary hover:underline"
								>/project/{user.name}/{encodeURIComponent(config.name)}</a
							>.
						</div>
						{#if !copyData}
							<div>
								Your Project does not contain any data, go to <a
									href={`https://zenoml.com/docs/python-client`}
									target="_blank"
									class="text-primary hover:underline">our docs</a
								> to learn how to add data to your project.
							</div>
						{:else if !copySystems}
							<div>
								Your Project does not contain system outputs, go to <a
									href={`https://zenoml.com/docs/python-client`}
									target="_blank"
									class="text-primary hover:underline">our docs</a
								> to learn how to add system outputs to your project.
							</div>
						{/if}
					</div>
				</div>
				<div class="flex items-center self-end">
					<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}
						>Ok</Button
					>
				</div>
			{/if}
		</div>
	</Content>
</Popup>
