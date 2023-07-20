<script lang="ts">
	import { ZenoService, type Organization, type User } from '$lib/zenoapi';
	import { mdiClose, mdiCog, mdiLogout, mdiPlus } from '@mdi/js';
	import { Icon } from '@smui/button';
	import { Svg } from '@smui/common';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { tooltip } from '@svelte-plugins/tooltips';
	import OrganizationPopup from '../popups/OrganizationPopup.svelte';

	export let organizations: Organization[];
	export let user: User;

	let organizationToEdit: Organization | undefined;
</script>

{#if organizationToEdit}
	<OrganizationPopup
		{organizationToEdit}
		{user}
		on:close={() => {
			organizationToEdit = undefined;
			ZenoService.getOrganizations(user).then(
				(fetchedOrganizations) => (organizations = fetchedOrganizations)
			);
		}}
	/>
{/if}
<div class="vertical mt">
	<div class="horizontal">
		<h2 class="mr">Organizations ({organizations.length})</h2>
		<IconButton
			on:click={() => {
				ZenoService.addOrganization({
					user: user,
					organization: { name: 'New Organization', id: -1, members: [], admin: true }
				}).then(() =>
					ZenoService.getOrganizations(user).then(
						(fetchedOrganizations) => (organizations = fetchedOrganizations)
					)
				);
			}}
		>
			<Icon component={Svg} viewBox="0 0 24 24">
				<path fill="black" d={mdiPlus} />
			</Icon>
		</IconButton>
	</div>
	{#if organizations.length > 0}
		<table>
			<thead>
				<th>Name</th>
				<th># Members</th>
				<th style="text-align: right;">Admin</th>
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
						<td>
							{organization.name}
						</td>
						<td>
							{organization.members.length}
						</td>
						<td>
							<div class="horizontal justify-end">
								<div
									use:tooltip={{
										content: 'Manage this organization. You can only do this if you are an admin.',
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
										<Icon component={Svg} viewBox="0 0 24 24">
											<path fill={organization.admin ? 'black' : 'grey'} d={mdiCog} />
										</Icon>
									</IconButton>
								</div>
								<div
									use:tooltip={{
										content:
											'Leave this organization. You can only do this if there is an admin left.',
										position: 'left',
										theme: 'zeno-tooltip'
									}}
								>
									<IconButton
										on:click={() => {
											const memberIndex = organization.members.findIndex(
												(currentMember) => currentMember.id === user.id
											);
											ZenoService.updateOrganization({
												...organization,
												members: [
													...organization.members.slice(0, memberIndex),
													...organization.members.slice(memberIndex + 1)
												]
											}).then(() =>
												ZenoService.getOrganizations(user).then((orgs) => (organizations = orgs))
											);
										}}
										disabled={organization.admin &&
											organization.members.filter((member) => member.admin).length < 2}
									>
										<Icon component={Svg} viewBox="0 0 24 24">
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
										content: 'Delete this organization. You can only do this if you are an admin.',
										position: 'left',
										theme: 'zeno-tooltip'
									}}
								>
									<IconButton
										on:click={() => {
											ZenoService.deleteOrganization(organization).then(() =>
												ZenoService.getOrganizations(user).then((orgs) => (organizations = orgs))
											);
										}}
										disabled={!organization.admin}
									>
										<Icon component={Svg} viewBox="0 0 24 24">
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

<style>
	.horizontal {
		display: flex;
		align-items: center;
	}

	.vertical {
		display: flex;
		flex-direction: column;
	}

	.mt {
		margin-top: 30px;
	}

	.mr {
		margin-right: 10px;
	}

	table {
		margin-top: 5px;
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

	td {
		padding-right: 10px;
	}

	.justify-end {
		justify-content: end;
	}
</style>
