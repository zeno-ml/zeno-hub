<script lang="ts">
	import { project } from '$lib/stores';
	import type { Organization, Project, User, ZenoService } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import Checkbox from '@smui/checkbox';
	import IconButton from '@smui/icon-button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher, getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import Popup from './Popup.svelte';

	export let config: Project;
	export let user: User;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let input: Textfield;
	let selectedUser: User | undefined;
	let selectedOrg: Organization | undefined;

	let projectUsers: User[] = [];
	let allUsers: User[] = [];
	zenoClient.getUsers().then((r) => (allUsers = r));
	zenoClient.getProjectUsers($project.uuid).then((r) => (projectUsers = r));
	let projectOrganizations: Organization[] = [];
	zenoClient.getProjectOrgs($project.uuid).then((r) => (projectOrganizations = r));

	$: availableUsers = allUsers.filter(
		(u) => u.id !== user.id && !projectUsers.some((member) => member.id === u.id)
	);

	$: invalidName = config.name.length === 0 || config.name.match(/[/]/g) !== null;
	$: if (input) {
		input.getElement().focus();
	}

	function updateProject() {
		zenoClient.updateProject(config).then(() => {
			dispatch('close');
		});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
	}

	function addUser(e: CustomEvent) {
		zenoClient
			.addProjectUser($project.uuid, {
				...e.detail,
				admin: false
			})
			.then(() => zenoClient.getProjectUsers($project.uuid).then((r) => (projectUsers = r)));
		selectedUser = undefined;
	}

	function addOrganization(e: CustomEvent) {
		zenoClient
			.addProjectOrg($project.uuid, {
				...e.detail,
				admin: false
			})
			.then(() => zenoClient.getProjectOrgs($project.uuid).then((r) => (projectOrganizations = r)));
		selectedOrg = undefined;
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content class="flex max-h-[80vh] w-[800px] flex-col overflow-y-auto">
		<h2 class="mb-4 text-xl">Project Settings</h2>
		<!--Project Settings-->
		<h3 class="text-lg">Settings</h3>
		<div class="mb-12 flex flex-col">
			<div class="mb-6 flex">
				<div class="mr-8 flex w-1/2 flex-col">
					<div>
						<Textfield bind:value={config.name} label="Name" bind:this={input} class="w-full" />
					</div>
					<div>
						<Textfield
							bind:value={config.samplesPerPage}
							label="Number of displayed items"
							bind:this={input}
							type="number"
							class="w-full"
						/>
					</div>
				</div>
				<div class="flex flex-col">
					<div class="flex items-center">
						<Checkbox checked={config.public} on:click={() => (config.public = !config.public)} />
						<span>Public visibility</span>
					</div>
					<span>Created: {new Date(config.createdAt ?? '').toLocaleString()}</span>
					<span>Updated: {new Date(config.updatedAt ?? '').toLocaleString()}</span>
				</div>
			</div>
			<div>
				<Textfield textarea bind:value={config.description} label="Description" class="w-full" />
			</div>
			<!--Visibility Settings-->
			<div class="mb-5 mt-12 flex flex-col" transition:fade>
				<h3 class="mb-2 text-lg">Viewers</h3>
				{#if projectUsers.length > 0}
					<table>
						<thead
							class="sticky left-0 top-0 border-b border-grey-lighter bg-background pb-1 font-semibold"
						>
							<th>Email</th>
							<th class="w-1">Editor</th>
							<th class="w-1" />
						</thead>
						<tbody>
							{#each projectUsers.sort((a, b) => {
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
												zenoClient
													.updateProjectUser($project.uuid, {
														...member,
														admin: !member.admin
													})
													.then(() =>
														zenoClient
															.getProjectUsers($project.uuid)
															.then((r) => (projectUsers = r))
													)}
											disabled={member.id === user.id}
										/>
									</td>
									<td class="text-end">
										{#if member.id !== user.id}
											<IconButton
												on:click={() =>
													zenoClient
														.deleteProjectUser($project.uuid, member)
														.then(() =>
															zenoClient
																.getProjectUsers($project.uuid)
																.then((r) => (projectUsers = r))
														)}
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
			</div>
			{#await zenoClient.getOrganizations() then oragnizationNames}
				{@const availableOrgs = oragnizationNames.filter(
					(currentOrg) => !projectOrganizations.some((org) => org.id === currentOrg.id)
				)}
				{#if availableOrgs.length > 0 || projectOrganizations.length > 0}
					<div class="mb-5 flex flex-col" transition:fade>
						<h3 class="mb-2 text-lg">Organizations</h3>
						{#if projectOrganizations.length > 0}
							<table>
								<thead>
									<th>Name</th>
									<th class="w-1">Editor</th>
									<th class="w-1" />
								</thead>
								<tbody>
									{#each projectOrganizations.sort((a, b) => {
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
														zenoClient
															.updateProjectOrg($project.uuid, {
																...org,
																admin: !org.admin
															})
															.then(() =>
																zenoClient
																	.getProjectOrgs($project.uuid)
																	.then((r) => (projectOrganizations = r))
															)}
												/>
											</td>
											<td class="text-end">
												<IconButton
													on:click={() =>
														zenoClient
															.deleteProjectOrg($project.uuid, org)
															.then(() =>
																zenoClient
																	.getProjectOrgs($project.uuid)
																	.then((r) => (projectOrganizations = r))
															)}
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
					</div>
				{/if}
			{/await}
			<div class="flex items-center self-end">
				<Button class="ml-4" variant="outlined" on:click={() => dispatch('close')}>Cancel</Button>
				<Button
					class="ml-2"
					variant="outlined"
					disabled={invalidName}
					on:click={() => updateProject()}>{'Update'}</Button
				>
			</div>
		</div>
	</Content>
</Popup>
