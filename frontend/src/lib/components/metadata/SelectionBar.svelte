<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { currentProject, editTag, metric, model, projectConfig } from '$lib/stores';
	import type { GroupMetric } from '$lib/zenoapi';
	import { mdiRefresh } from '@mdi/js';
	import Button, { Group, Icon } from '@smui/button';
	import CircularProgress from '@smui/circular-progress';
	import { Svg } from '@smui/common';
	import { tooltip } from '@svelte-plugins/tooltips';
	import ChipsWrapper from './ChipsWrapper.svelte';

	export let currentResult: GroupMetric[] | undefined;
	export let selected = 'list';

	let CHOICES: string[];

	let runningAnalysis = true;

	$: CHOICES =
		$editTag === undefined
			? $projectConfig !== undefined && $projectConfig.view !== ''
				? ['list', 'table']
				: ['table']
			: ['table'];

	$: {
		if ($projectConfig === undefined) {
			runningAnalysis = true;
		} else {
			runningAnalysis = false;
		}
	}
</script>

<div style:width="100%">
	<div class="between">
		<ChipsWrapper />
		<div class="status inline">
			{#if runningAnalysis}
				<CircularProgress
					class="status-circle"
					style="height: 32px; width: 32px; margin-right:20px"
					indeterminate
				/>
			{:else}
				<div
					on:keydown={() => ({})}
					on:click={() => invalidateAll()}
					use:tooltip={{
						content: 'Refresh data & functions',
						position: 'left',
						theme: 'zeno-tooltip'
					}}
				>
					<div class="icon">
						<Icon style="outline:none" component={Svg} viewBox="0 0 24 24">
							<path d={mdiRefresh} />
						</Icon>
					</div>
				</div>
			{/if}
		</div>
	</div>
	{#if !$page.url.href.includes('compare')}
		<div class="options">
			<div>
				{#if currentResult}
					{#if currentResult[0].metric !== undefined && currentResult[0].metric !== null}
						<span class="metric">
							{$metric ? $metric.name + ':' : ''}
						</span>
						<span class="metric-value">
							{currentResult[0].metric.toFixed(2)}
						</span>
					{/if}
					<span id="size">({currentResult[0].size.toLocaleString()} instances)</span>
				{/if}
			</div>
			<div class="inline">
				{#if $editTag === undefined}
					<slot />
					<Group>
						{#if $model !== undefined && $currentProject !== undefined}
							{#each CHOICES as choice}
								<Button
									style="background-color: {selected === choice ? 'var(--G5)' : 'var(--G6)'}"
									variant="outlined"
									on:click={() => (selected = choice)}>{choice}</Button
								>
							{/each}
						{/if}
					</Group>
				{:else}
					<div class="inline" style="margin-right: 10px">
						<p style="margin: auto; margin-right: 10px">Editing</p>
						<div class="meta-chip">{$editTag.tagName}</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	p {
		margin: 0px;
	}
	.icon {
		cursor: pointer;
		width: 24px;
		height: 24px;
		fill: var(--G1);
	}
	.between {
		padding-top: 10px;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		width: 100%;
		border-bottom: 1px solid var(--G5);
	}
	.options {
		display: flex;
		flex-direction: inline;
		flex-wrap: wrap;
		justify-content: space-between;
		width: 100%;
		align-items: center;
		padding-top: 10px;
		padding-bottom: 10px;
		border-bottom: 1px solid var(--G5);
	}
	.metric {
		font-weight: 400;
		color: var(--G2);
		margin-right: 15px;
	}
	.metric-value {
		font-weight: 400;
		color: var(--logo);
		margin-right: 15px;
	}
	#size {
		font-style: italic;
		color: var(--G3);
		margin-right: 10px;
	}
	.inline {
		display: flex;
		align-items: center;
	}
	.meta-chip {
		padding: 5px 10px;
		background: var(--N2);
		margin-left: 5px;
		margin-right: 5px;
		margin-top: 2px;
		margin-bottom: 2px;
		border-radius: 4px;
		width: fit-content;
		margin: auto;
	}
</style>
