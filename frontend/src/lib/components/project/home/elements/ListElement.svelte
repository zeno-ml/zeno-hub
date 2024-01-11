<script>
	import { goto } from '$app/navigation';
	import ListView from '$lib/components/instances/ListView.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import { columns, model, models, project, sort } from '$lib/stores';
	import Button from '@smui/button/src/Button.svelte';

	$: sortedModels = $models.sort((a, b) => a.localeCompare(b));
</script>

<div class="flex min-h-0 w-full min-w-0 items-center pb-2">
	<p class="mr-2 font-semibold text-grey-dark">model:</p>
	<Select
		bind:value={$model}
		options={[
			...sortedModels.map((model) => {
				return { value: model, label: model };
			})
		]}
	/>
	<p class="ml-2 mr-2 font-semibold text-grey-dark">sort by:</p>
	<Select
		bind:value={$sort[0]}
		options={[
			...$columns.map((column) => {
				return { value: column, label: column.name };
			})
		]}
	/>
	<div class="ml-2">
		<Select
			bind:value={$sort[1]}
			options={[
				{ value: true, label: 'ascending' },
				{ value: false, label: 'descending' }
			]}
		/>
	</div>
	<Button
		on:click={() => goto(`/project/${$project.uuid}/${encodeURIComponent($project.name)}/explore`)}
		class="ml-auto">Explore</Button
	>
</div>
<div class="flex h-full min-h-0 flex-col">
	<ListView />
</div>
