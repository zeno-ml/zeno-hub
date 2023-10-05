<script lang="ts">
	import { report } from '$lib/stores';
	import { ZenoService, type Organization, type Report, type User } from '$lib/zenoapi';
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

	export let reportConfig: Report;
	export let user: User;

	const dispatch = createEventDispatcher();

	let input: Textfield;
	let selectedUser: User | undefined;
	let selectedOrg: Organization | undefined;

	let userRequest = ZenoService.getReportUsers($report.id);
	let organizationRequest = ZenoService.getReportOrgs($report.id);

	$: invalidName = reportConfig.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	function updateReport() {
		ZenoService.updateReport(reportConfig).then(() => {
			report.set(reportConfig);
			dispatch('close');
		});
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			updateReport();
		}
	}

	function addUser(e: CustomEvent) {
		ZenoService.addReportUser($report.id, {
			...e.detail,
			admin: false
		}).then(() => (userRequest = ZenoService.getReportUsers($report.id)));
		selectedUser = undefined;
	}

	function addOrganization(e: CustomEvent) {
		ZenoService.addReportOrg($report.id, {
			...e.detail,
			admin: false
		}).then(() => (organizationRequest = ZenoService.getReportOrgs($report.id)));
		selectedOrg = undefined;
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; flex-direction: column; width: 800px;">
		<h2 class="text-xl mb-4">Report Administration</h2>
		<h3 class="text-lg">Settings</h3>
		<div class="mb-12 flex flex-col">
			<div class="flex mb-6">
				<div class="flex flex-col mr-8">
					<div>
						<Textfield bind:value={reportConfig.name} label="Name" bind:this={input} />
					</div>
				</div>
				<div class="flex flex-col">
					<div class="flex items-center">
						<Checkbox
							checked={reportConfig.public}
							on:click={() => (reportConfig.public = !reportConfig.public)}
						/>
						<span>Public visibility</span>
					</div>
				</div>
			</div>
			<Textfield
				textarea
				bind:value={reportConfig.description}
				label="Description"
				style="width: 100%"
			/>
		</div>
		{#if userRequest}
			{#await userRequest then currentUsers}
				<div class="mb-5 flex flex-col" transition:fade>
					<h3 class="text-lg mb-2">Viewers</h3>
					{#if currentUsers.length > 0}
						<table>
							<thead
								class="border-b border-grey-lighter pb-1 top-0 left-0 sticky bg-background font-semibold"
							>
								<th>Email</th>
								<th class="w-1">Admin</th>
								<th class="w-1" />
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
													ZenoService.updateReportUser($report.id, {
														...member,
														admin: !member.admin
													}).then(() => (userRequest = ZenoService.getReportUsers($report.id)))}
												disabled={member.id === user.id}
											/>
										</td>
										<td style="text-align: end;">
											{#if member.id !== user.id}
												<IconButton
													on:click={() =>
														ZenoService.deleteReportUser($report.id, member).then(
															() => (userRequest = ZenoService.getReportUsers($report.id))
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
		{#if organizationRequest}
			{#await organizationRequest then currentOrgs}
				<div class="mb-5 flex flex-col" transition:fade>
					<h3 class="text-lg mb-2">Organizations</h3>
					{#if currentOrgs.length > 0}
						<table>
							<thead>
								<th>Name</th>
								<th class="w-1">Admin</th>
								<th class="w-1" />
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
													ZenoService.updateReportOrg($report.id, {
														...org,
														admin: !org.admin
													}).then(
														() => (organizationRequest = ZenoService.getReportOrgs($report.id))
													)}
											/>
										</td>
										<td style="text-align: end;">
											<IconButton
												on:click={() =>
													ZenoService.deleteReportOrg($report.id, org).then(
														() => (organizationRequest = ZenoService.getReportOrgs($report.id))
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
				on:click={() => updateReport()}>{'Update'}</Button
			>
		</div>
	</Content>
</Popup>
