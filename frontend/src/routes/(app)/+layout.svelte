<script lang="ts">
	import { goto } from '$app/navigation';
	import { navigating, page } from '$app/stores';
	import ProjectPopup from '$lib/components/popups/ProjectPopup.svelte';
	import { projectConfig } from '$lib/stores';
	import { getProjectRouteFromURL } from '$lib/util/util';
	import {
		mdiAccount,
		mdiChartBoxOutline,
		mdiCog,
		mdiCompare,
		mdiCompassOutline,
		mdiLogout
	} from '@mdi/js';
	import IconButton, { Icon } from '@smui/icon-button';
	import { tooltip } from '@svelte-plugins/tooltips';

	export let data;

	let projectEdit = false;
</script>

{#if projectEdit && $projectConfig}
	<ProjectPopup project={$projectConfig} on:close={() => (projectEdit = false)} user={data.user} />
{/if}
<main>
	<nav>
		<header>
			<div class="inline">
				<a href="/">
					<img style="width:30px" src="/zeno.png" alt="Square spiral logo next to 'Zeno'" />
				</a>
				{#if $page.url.href.includes('project')}
					<div id="tabs">
						<div
							class="item {$page.url.href.includes('explore') ? 'selected' : ''}"
							on:keydown={() => ({})}
							on:click={() => {
								goto(`${getProjectRouteFromURL($page.url)}/explore`);
							}}
							use:tooltip={{
								content: 'Explore your data and model outputs.',
								position: 'right',
								theme: 'zeno-tooltip'
							}}
						>
							<div class="icon">
								<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
									<path
										fill={$page.url.href.includes('explore') ? '#6a1b9a' : 'black'}
										d={mdiCompassOutline}
									/>
								</Icon>
							</div>
						</div>
						<div
							class="item {$page.url.href.includes('compare') ? 'selected' : ''}"
							on:keydown={() => ({})}
							on:click={() => {
								goto(`${getProjectRouteFromURL($page.url)}/compare`);
							}}
							use:tooltip={{
								content: 'Qualitatively compare model outputs',
								position: 'right',
								theme: 'zeno-tooltip'
							}}
						>
							<div class="icon">
								<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
									<path
										fill={$page.url.href.includes('compare') ? '#6a1b9a' : 'black'}
										d={mdiCompare}
									/>
								</Icon>
							</div>
						</div>
						<div
							class="item {$page.url.href.includes('chart') ? 'selected' : ''}"
							on:keydown={() => ({})}
							on:click={() => {
								goto(`${getProjectRouteFromURL($page.url)}/chart`);
							}}
							use:tooltip={{
								content: 'Create charts from your slices and metrics.',
								position: 'right',
								theme: 'zeno-tooltip'
							}}
						>
							<div class="icon">
								<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
									<path
										fill={$page.url.href.includes('chart') ? '#6a1b9a' : 'black'}
										d={mdiChartBoxOutline}
									/>
								</Icon>
							</div>
						</div>
						{#if $projectConfig && $projectConfig.editor}
							<div
								class="item"
								on:keydown={() => ({})}
								on:click={() => {
									projectEdit = true;
								}}
								use:tooltip={{
									content: "Edit your project's configuration.",
									position: 'right',
									theme: 'zeno-tooltip'
								}}
							>
								<div class="icon">
									<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
										<path
											fill={$page.url.href.includes('chart') ? '#6a1b9a' : 'black'}
											d={mdiCog}
										/>
									</Icon>
								</div>
							</div>
						{/if}
					</div>
				{/if}
			</div>

			<div class="icons">
				<IconButton on:click={() => goto('/account')}>
					<Icon tag="svg" viewBox="0 0 24 24">
						<path fill="black" d={mdiAccount} />
					</Icon>
				</IconButton>
				<form method="POST" action="/logout">
					<IconButton>
						<Icon tag="svg" viewBox="0 0 24 24">
							<path fill="black" d={mdiLogout} />
						</Icon>
					</IconButton>
				</form>
			</div>
		</header>
	</nav>
	{#if Boolean($navigating)}
		<div class="container centered">
			<p>Loading...</p>
		</div>
	{:else}
		<slot />
	{/if}
</main>

<style>
	main {
		display: flex;
		flex-direction: row;
		text-align: left;
		width: 100%;
		height: 100%;
	}

	.container {
		width: 100%;
		height: 100%;
	}

	.centered {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	header {
		height: 100vh;
		width: 50px;
		display: flex;
		color: var(--G1);
		flex-direction: column;
		justify-content: space-between;
		background: var(--Y1);
	}

	img {
		align-self: center;
		margin-top: 30px;
		margin-bottom: 10px;
	}

	.inline {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.icon {
		width: 24px;
		height: 24px;
		fill: var(--G1);
	}
	.icons {
		margin: 0px auto;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.item {
		margin: 0px auto;
		display: flex;
		align-items: center;
		cursor: pointer;
		padding-left: 10px;
		padding-right: 10px;
		padding-top: 10px;
		padding-bottom: 10px;
	}

	.item:hover {
		background-color: rgb(0, 0, 0, 0.05);
	}

	.selected {
		color: var(--logo);
		font-weight: 500;
	}

	#tabs {
		display: flex;
		flex-direction: column;
		margin-top: 10px;
	}
</style>
