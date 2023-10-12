<script lang="ts">
	import type { Organization, User, ZenoService } from '$lib/zenoapi';
	import { mdiClose, mdiCog, mdiLogout, mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { tooltip } from '@svelte-plugins/tooltips';
	import { getContext } from 'svelte';
	import OrganizationPopup from '../popups/OrganizationPopup.svelte';

	export let organizations: Organization[];
	export let user: User;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let organizationToEdit: Organization | undefined;
</script>

{#if organizationToEdit}
	<OrganizationPopup
		{organizationToEdit}
		{user}
		on:close={() => {
			organizationToEdit = undefined;
			zenoClient
				.getOrganizations()
				.then((fetchedOrganizations) => (organizations = fetchedOrganizations));
		}}
	/>
{/if}
<div class="flex flex-col mt-7">
	<div class="flex items-center">
		<h2 class="mr-2.5 text-lg">Organizations ({organizations.length})</h2>
		<IconButton
			on:click={() => {
				zenoClient
					.addOrganization({
						user: user,
						organization: { name: 'New Organization', id: -1, members: [], admin: true }
					})
					.then(() =>
						zenoClient
							.getOrganizations()
							.then((fetchedOrganizations) => (organizations = fetchedOrganizations))
					);
			}}
		>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={mdiPlus} />
			</Icon>
		</IconButton>
	</div>
	{#if organizations.length > 0}
		<table class="mt-1">
			<thead class="border-b border-grey-lighter pb-2 top-0 left-0 sticky bg-background">
				<th>Name</th>
				<th># Members</th>
				<th class="text-right">Admin</th>
			</thead>
			<tbody>
				{#each organizations.sort((a, b) => {
					if (a.admin && !b.admin) {
						return -1;
					} else if (!a.admin && b.admin) {
						return 1;
					}
					return a.name.localeCompare(b.name);
				}) as organization}
					<tr>
						<td class="pr-2.5">
							{organization.name}
						</td>
						<td class="pr-2.5">
							{organization.members.length}
						</td>
						<td class="pr-2.5">
							<div class="flex items-center justify-end">
								<div
									use:tooltip={{
										content: 'Manage this organization. You can only do this if you are an admin',
										position: 'left',
										theme: 'zeno-tooltip'
									}}
								>
									<IconButton
										on:click={() => {
											organizationToEdit = organization;
										}}
										disabled={!organization.admin}
									>
										<Icon tag="svg" viewBox="0 0 24 24">
											<path fill={organization.admin ? 'black' : 'grey'} d={mdiCog} />
										</Icon>
									</IconButton>
								</div>
								<div
									use:tooltip={{
										content:
											'Leave this organization. You can only do this if there is an admin left',
										position: 'left',
										theme: 'zeno-tooltip'
									}}
								>
									<IconButton
										on:click={() => {
											const memberIndex = organization.members.findIndex(
												(currentMember) => currentMember.id === user.id
											);
											zenoClient
												.updateOrganization({
													...organization,
													members: [
														...organization.members.slice(0, memberIndex),
														...organization.members.slice(memberIndex + 1)
													]
												})
												.then(() =>
													zenoClient.getOrganizations().then((orgs) => (organizations = orgs))
												);
										}}
										disabled={organization.admin &&
											organization.members.filter((member) => member.admin).length < 2}
									>
										<Icon tag="svg" viewBox="0 0 24 24">
											<path
												fill={organization.admin &&
												organization.members.filter((member) => member.admin).length < 2
													? 'grey'
													: 'black'}
												d={mdiLogout}
											/>
										</Icon>
									</IconButton>
								</div>
								<div
									use:tooltip={{
										content: 'Delete this organization. You can only do this if you are an admin',
										position: 'left',
										theme: 'zeno-tooltip'
									}}
								>
									<IconButton
										on:click={() => {
											zenoClient
												.deleteOrganization(organization)
												.then(() =>
													zenoClient.getOrganizations().then((orgs) => (organizations = orgs))
												);
										}}
										disabled={!organization.admin}
									>
										<Icon tag="svg" viewBox="0 0 24 24">
											<path fill={organization.admin ? 'black' : 'grey'} d={mdiClose} />
										</Icon>
									</IconButton>
								</div>
							</div>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
</div>
