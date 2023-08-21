<script lang="ts">
	import { project } from '$lib/stores';
	import { ZenoService, type Organization, type Project, type User } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';
	import Popup from './Popup.svelte';

	export let config: Project;
	export let user: User;

	const dispatch = createEventDispatcher();

	let input: Textfield;
	let selectedUser: User | undefined;
	let selectedOrg: Organization | undefined;

	let userRequest = $project ? ZenoService.getProjectUsers($project.uuid) : undefined;
	let organizationRequest = $project ? ZenoService.getProjectOrgs($project.uuid) : undefined;

	$: invalidName = config.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	function updateProject() {
		ZenoService.updateProject(config).then(() => {
			project.set(config);
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

	function addUser(e: CustomEvent) {
		$project &&
			ZenoService.addProjectUser($project.uuid, {
				...e.detail,
				admin: false
			}).then(() => {
				if ($project) {
					userRequest = ZenoService.getProjectUsers($project.uuid);
				}
			});
		selectedUser = undefined;
	}

	function addOrganization(e: CustomEvent) {
		$project &&
			ZenoService.addProjectOrg($project.uuid, {
				...e.detail,
				admin: false
			}).then(() => {
				if ($project) {
					organizationRequest = ZenoService.getProjectOrgs($project.uuid);
				}
			});
		selectedOrg = undefined;
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; flex-direction: column; width: 800px;">
		<h2>Project Aministration</h2>
		<div class="mb-5 flex flex-col">
			<div>
				<Textfield bind:value={config.name} label="Name" bind:this={input} />
			</div>
			<div>
				<Textfield
					bind:value={config.samplesPerPage}
					label="Number of displayed items"
					bind:this={input}
					type="number"
				/>
			</div>
			<div class="flex items-center">
				<span>Calculate histogram metrics</span>
				<Checkbox
					checked={config.calculateHistogramMetrics}
					on:click={() => (config.calculateHistogramMetrics = !config.calculateHistogramMetrics)}
				/>
			</div>
			<div class="flex items-center">
				<span>Public project</span>
				<Checkbox checked={config.public} on:click={() => (config.public = !config.public)} />
			</div>
		</div>
		{#if !config.public && userRequest}
			{#await userRequest then currentUsers}
				<div class="mb-5 flex flex-col" transition:fade>
					<h3>Users</h3>
					{#if currentUsers.length > 0}
						<table>
							<thead
								class="border-b border-grey-lighter pb-1 top-0 left-0 sticky bg-background font-semibold"
							>
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
									else return 0;
								}) as member}
									<tr>
										<td>
											{member.name}
										</td>
										<td>
											<Checkbox
												checked={member.admin}
												on:click={() =>
													$project &&
													ZenoService.updateProjectUser($project.uuid, {
														...member,
														admin: !member.admin
													}).then(() => {
														if ($project) {
															userRequest = ZenoService.getProjectUsers($project.uuid);
														}
													})}
												disabled={member.id === user.id}
											/>
										</td>
										<td style="text-align: end;">
											{#if member.id !== user.id}
												<IconButton
													on:click={() =>
														$project &&
														ZenoService.deleteProjectUser($project.uuid, member).then(() => {
															if ($project) {
																userRequest = ZenoService.getProjectUsers($project.uuid);
															}
														})}
												>
													<Icon tag="svg" viewBox="0 0 24 24">
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
								on:change={addUser}
								options={availableUsers}
								placeholder="add collaborators"
								searchable={true}
							/>
						{/if}
					{/await}
				</div>
			{/await}
		{/if}
		{#if !config.public && organizationRequest}
			{#await organizationRequest then currentOrgs}
				<div class="mb-5 flex flex-col" transition:fade>
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
													$project &&
													ZenoService.updateProjectOrg($project.uuid, {
														...org,
														admin: !org.admin
													}).then(() => {
														if ($project) {
															organizationRequest = ZenoService.getProjectOrgs($project.uuid);
														}
													})}
											/>
										</td>
										<td style="text-align: end;">
											<IconButton
												on:click={() =>
													$project &&
													ZenoService.deleteProjectOrg($project.uuid, org).then(() => {
														if ($project) {
															organizationRequest = ZenoService.getProjectOrgs($project.uuid);
														}
													})}
											>
												<Icon tag="svg" viewBox="0 0 24 24">
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
								on:change={addOrganization}
								options={availableOrgs}
								placeholder="add organization access"
								searchable={true}
							/>
						{/if}
					{/await}
				</div>
			{/await}
		{/if}
		<div class="flex items-center self-end">
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
