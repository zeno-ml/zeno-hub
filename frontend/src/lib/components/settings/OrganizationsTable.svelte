<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { tooltip } from '$lib/util/tooltip';
	import type { Organization, User, ZenoService } from '$lib/zenoapi';
	import { mdiClose, mdiCog, mdiLogout, mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import IconButton from '@smui/icon-button';
	import { getContext } from 'svelte';
	import Confirm from '../popups/Confirm.svelte';
	import NewOrganizationPopup from '../popups/NewOrganizationPopup.svelte';
	import OrganizationPopup from '../popups/OrganizationPopup.svelte';

	export let organizations: Organization[];
	export let user: User;

	const zenoClient = getContext('zenoClient') as ZenoService;

	let organizationToEdit: Organization | undefined;
	let showConfirmDelete = false;
	let showNewOrganizationPopup = false;
	let organizationToDelete: Organization | undefined;
</script>

{#if showNewOrganizationPopup}
	<NewOrganizationPopup {user} on:close={() => (showNewOrganizationPopup = false)} />
{/if}
{#if organizationToEdit}
	<OrganizationPopup
		{organizationToEdit}
		{user}
		on:close={() => {
			organizationToEdit = undefined;
			invalidate('app:organizations');
		}}
	/>
{/if}
{#if showConfirmDelete}
	<Confirm
		message="Are you sure you want to delete this organization?"
		on:cancel={() => {
			showConfirmDelete = false;
		}}
		on:confirm={() => {
			if (organizationToDelete !== undefined) {
				zenoClient
					.deleteOrganization(organizationToDelete)
					.then(() => invalidate('app:organizations'));
			}
			showConfirmDelete = false;
		}}
	/>
{/if}
<div class="mt-7 flex flex-col">
	<div class="flex items-center">
		<h2 class="mr-2.5 text-lg">Organizations ({organizations.length})</h2>
		<IconButton on:click={() => (showNewOrganizationPopup = true)}>
			<Icon tag="svg" viewBox="0 0 24 24">
				<path fill="black" d={mdiPlus} />
			</Icon>
		</IconButton>
	</div>
	{#if organizations.length > 0}
		<table class="mt-1">
			<thead class="sticky left-0 top-0 border-b border-grey-lighter bg-background pb-2">
				<th>Name</th>
				<th># Members</th>
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
										text: 'Manage this organization. You can only do this if you are an admin'
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
										text: 'Leave this organization. You can only do this if there is an admin left'
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
												.then(() => invalidate('app:organizations'));
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
										text: 'Delete this organization. You can only do this if you are an admin'
									}}
								>
									<IconButton
										on:click={() => {
											organizationToDelete = organization;
											showConfirmDelete = true;
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
