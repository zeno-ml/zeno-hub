<script lang="ts">
	import { projectConfig } from '$lib/stores';
	import { ZenoService, type Organization, type ProjectConfig, type User } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import { Svg } from '@smui/common';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';
	import Popup from './Popup.svelte';

	export let project: ProjectConfig;
	export let user: User;

	const dispatch = createEventDispatcher();

	let input: Textfield;
	let selectedUser: User | undefined;
	let selectedOrg: Organization | undefined;

	let userRequest = $projectConfig ? ZenoService.getProjectUsers($projectConfig.uuid) : undefined;
	let organizationRequest = $projectConfig
		? ZenoService.getProjectOrgs($projectConfig.uuid)
		: undefined;

	$: invalidName = project.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	function updateProject() {
		ZenoService.updateProject(project).then(() => {
			projectConfig.set(project);
			dispatch('close');
		});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			updateProject();
		}
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; flex-direction: column; width: 800px;">
		<h2>Project Aministration</h2>
		<div class="element">
			<div>
				<Textfield bind:value={project.name} label="Name" bind:this={input} />
			</div>
			<div>
				<Textfield
					bind:value={project.numItems}
					label="Number of displayed items"
					bind:this={input}
					type="number"
				/>
			</div>
			<div class="horizontal">
				<span>Calculate histogram metrics</span>
				<Checkbox
					checked={project.calculateHistogramMetrics}
					on:click={() => (project.calculateHistogramMetrics = !project.calculateHistogramMetrics)}
				/>
			</div>
			<div class="horizontal">
				<span>Public project</span>
				<Checkbox checked={project.public} on:click={() => (project.public = !project.public)} />
			</div>
		</div>
		{#if !project.public && userRequest}
			{#await userRequest then currentUsers}
				<div class="element" transition:fade>
					<h3>Users</h3>
					{#if currentUsers.length > 0}
						<table>
							<thead>
								<th>Name</th>
								<th>Email</th>
								<th>Admin</th>
								<th />
							</thead>
							<tbody>
								{#each currentUsers.sort((a, b) => {
									if (a.id === user.id) return -1;
									else if (b.id === user.id) return 1;
									else if (a.admin && !b.admin) return -1;
									else if (!a.admin && b.admin) return 1;
									return a.name && b.name ? a.name.localeCompare(b.name) : 0;
								}) as member}
									<tr>
										<td>
											{member.name}
										</td>
										<td>
											{member.email}
										</td>
										<td>
											<Checkbox
												checked={member.admin}
												on:click={() =>
													$projectConfig &&
													ZenoService.updateProjectUser($projectConfig.uuid, {
														...member,
														admin: !member.admin
													}).then(() => {
														if ($projectConfig) {
															userRequest = ZenoService.getProjectUsers($projectConfig.uuid);
														}
													})}
												disabled={member.id === user.id}
											/>
										</td>
										<td style="text-align: end;">
											{#if member.id !== user.id}
												<IconButton
													on:click={() =>
														$projectConfig &&
														ZenoService.deleteProjectUser($projectConfig.uuid, member).then(() => {
															if ($projectConfig) {
																userRequest = ZenoService.getProjectUsers($projectConfig.uuid);
															}
														})}
												>
													<Icon component={Svg} viewBox="0 0 24 24">
														<path fill="black" d={mdiClose} />
													</Icon>
												</IconButton>
											{/if}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{/if}
					{#await ZenoService.getUsers() then users}
						{@const availableUsers = users.filter(
							(currentUser) =>
								!(
									currentUser.id === user.id ||
									currentUsers.some((member) => member.id === currentUser.id)
								)
						)}
						{#if availableUsers.length > 0}
							<Svelecte
								style="width: 280px; height: 30px; flex:none; align-self: end; margin-bottom: 20px;"
								bind:value={selectedUser}
								on:change={(e) => {
									$projectConfig &&
										ZenoService.addProjectUser($projectConfig.uuid, {
											...e.detail,
											admin: false
										}).then(() => {
											if ($projectConfig) {
												userRequest = ZenoService.getProjectUsers($projectConfig.uuid);
											}
										});
									selectedUser = undefined;
								}}
								options={availableUsers}
								placeholder="add collaborators"
								searchable={true}
							/>
						{/if}
					{/await}
				</div>
			{/await}
		{/if}
		{#if !project.public && organizationRequest}
			{#await organizationRequest then currentOrgs}
				<div class="element" transition:fade>
					<h3>Organizations</h3>
					{#if currentOrgs.length > 0}
						<table>
							<thead>
								<th>Name</th>
								<th>Admin</th>
								<th />
							</thead>
							<tbody>
								{#each currentOrgs.sort((a, b) => {
									if (a.admin && !b.admin) return -1;
									else if (!a.admin && b.admin) return 1;
									return a.name && b.name ? a.name.localeCompare(b.name) : 0;
								}) as org}
									<tr>
										<td>
											{org.name}
										</td>
										<td>
											<Checkbox
												checked={org.admin}
												on:click={() =>
													$projectConfig &&
													ZenoService.updateProjectOrg($projectConfig.uuid, {
														...org,
														admin: !org.admin
													}).then(() => {
														if ($projectConfig) {
															organizationRequest = ZenoService.getProjectOrgs($projectConfig.uuid);
														}
													})}
											/>
										</td>
										<td style="text-align: end;">
											<IconButton
												on:click={() =>
													$projectConfig &&
													ZenoService.deleteProjectOrg($projectConfig.uuid, org).then(() => {
														if ($projectConfig) {
															organizationRequest = ZenoService.getProjectOrgs($projectConfig.uuid);
														}
													})}
											>
												<Icon component={Svg} viewBox="0 0 24 24">
													<path fill="black" d={mdiClose} />
												</Icon>
											</IconButton>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					{/if}
					{#await ZenoService.getOrganizationNames() then oragnizationNames}
						{@const availableOrgs = oragnizationNames.filter(
							(currentOrg) => !currentOrgs.some((org) => org.id === currentOrg.id)
						)}
						{#if availableOrgs.length > 0}
							<Svelecte
								style="width: 280px; height: 30px; flex:none; align-self: end; margin-bottom: 20px;"
								bind:value={selectedOrg}
								on:change={(e) => {
									$projectConfig &&
										ZenoService.addProjectOrg($projectConfig.uuid, {
											...e.detail,
											admin: false
										}).then(() => {
											if ($projectConfig) {
												organizationRequest = ZenoService.getProjectOrgs($projectConfig.uuid);
											}
										});
									selectedUser = undefined;
								}}
								options={availableOrgs}
								placeholder="add organization access"
								searchable={true}
							/>
						{/if}
					{/await}
				</div>
			{/await}
		{/if}
		<div id="submit">
			<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}
				>Cancel</Button
			>
			<Button
				style="margin-left: 5px;"
				variant="outlined"
				disabled={invalidName}
				on:click={() => updateProject()}>{'Update'}</Button
			>
		</div>
	</Content>
</Popup>

<style>
	#submit {
		display: flex;
		align-items: center;
		align-self: end;
	}

	.horizontal {
		display: flex;
		align-items: center;
	}

	.element {
		margin-bottom: 20px;
		display: flex;
		flex-direction: column;
	}

	th {
		text-align: left;
		border-bottom: 1px solid var(--G5);
		padding-bottom: 5px;
		top: 0;
		left: 0;
		position: sticky;
		background-color: var(--G6);
		min-width: 70px;
		padding-right: 1.6vw;
		vertical-align: top;
		font-weight: 600;
		z-index: 5;
	}
</style>
