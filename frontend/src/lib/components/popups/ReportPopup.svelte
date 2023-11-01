<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import type { Organization, Report, User, ZenoService } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher, getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import Popup from './Popup.svelte';

	export let user: User;

	let report = $page.data.report as Report;

	const zenoClient = getContext('zenoClient') as ZenoService;
	const dispatch = createEventDispatcher();

	let input: Textfield;
	let selectedUser: User | undefined;
	let selectedOrg: Organization | undefined;

	let reportUsers: User[] = [];
	let allUsers: User[] = [];
	zenoClient.getUsers().then((r) => (allUsers = r));
	zenoClient.getReportUsers(report.id).then((r) => (reportUsers = r));
	let reportOrganizations: Organization[] = [];
	let allOrganizations: Organization[] = [];
	zenoClient.getReportOrgs(report.id).then((r) => (reportOrganizations = r));
	zenoClient.getOrganizationNames().then((r) => (allOrganizations = r));

	$: availableUsers = allUsers.filter(
		(u) => u.id !== user.id && !reportUsers.some((member) => member.id === u.id)
	);
	$: availableOrgs = allOrganizations.filter(
		(currentOrg) => !reportOrganizations.some((org) => org.id === currentOrg.id)
	);

	$: invalidName = report.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	async function updateReport() {
		await zenoClient.updateReport(report);
		goto(`/report/${report.ownerName}/${encodeURI(report.name)}`);
		dispatch('close');
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
		zenoClient
			.addReportUser(report.id, {
				...e.detail,
				admin: false
			})
			.then(() => zenoClient.getReportUsers(report.id).then((r) => (reportUsers = r)));
		selectedUser = undefined;
	}

	function addOrganization(e: CustomEvent) {
		zenoClient
			.addReportOrg(report.id, {
				...e.detail,
				admin: false
			})
			.then(() => zenoClient.getReportOrgs(report.id).then((r) => (reportOrganizations = r)));
		selectedOrg = undefined;
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content
		style="display: flex; flex-direction: column; width: 800px; max-height: 80vh; overflow-y: scroll"
	>
		<h2 class="mb-4 text-xl">Report Settings</h2>
		<h3 class="text-lg">Settings</h3>
		<div class="mb-12 flex flex-col">
			<div class="mb-6 flex">
				<div class="mr-8 flex flex-col">
					<div>
						<Textfield bind:value={report.name} label="Name" bind:this={input} />
					</div>
				</div>
				<div class="flex flex-col">
					<div class="flex items-center">
						<Checkbox checked={report.public} on:click={() => (report.public = !report.public)} />
						<span>Public visibility</span>
					</div>
					<span>Created: {new Date(report.createdAt ?? '').toLocaleString()}</span>
					<span>Updated: {new Date(report.updatedAt ?? '').toLocaleString()}</span>
				</div>
			</div>
			<Textfield textarea bind:value={report.description} label="Description" style="width: 100%" />
		</div>
		<div class="mb-5 flex flex-col" transition:fade>
			<h3 class="mb-2 text-lg">Collaborators</h3>
			{#if reportUsers.length > 0}
				<table>
					<thead
						class="sticky left-0 top-0 border-b border-grey-lighter bg-background pb-1 font-semibold"
					>
						<th>Email</th>
						<th class="w-1">Editor</th>
						<th class="w-1" />
					</thead>
					<tbody>
						{#each reportUsers.sort((a, b) => {
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
												.updateReportUser(report.id, {
													...member,
													admin: !member.admin
												})
												.then(() =>
													zenoClient.getReportUsers(report.id).then((r) => (reportUsers = r))
												)}
										disabled={member.id === user.id}
									/>
								</td>
								<td style="text-align: end;">
									{#if member.id !== user.id}
										<IconButton
											on:click={() =>
												zenoClient
													.deleteReportUser(report.id, member)
													.then(() =>
														zenoClient.getReportUsers(report.id).then((r) => (reportUsers = r))
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
		<div class="mb-5 flex flex-col" transition:fade>
			<h3 class="mb-2 text-lg">Organizations</h3>
			{#if reportOrganizations.length > 0}
				<table>
					<thead
						class="sticky left-0 top-0 border-b border-grey-lighter bg-background pb-1 font-semibold"
					>
						<th>Name</th>
						<th class="w-1">Editor</th>
						<th class="w-1" />
					</thead>
					<tbody>
						{#each reportOrganizations.sort((a, b) => {
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
												.updateReportOrg(report.id, {
													...org,
													admin: !org.admin
												})
												.then(() =>
													zenoClient.getReportOrgs(report.id).then((r) => (reportOrganizations = r))
												)}
									/>
								</td>
								<td style="text-align: end;">
									<IconButton
										on:click={() =>
											zenoClient
												.deleteReportOrg(report.id, org)
												.then(() =>
													zenoClient.getReportOrgs(report.id).then((r) => (reportOrganizations = r))
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
