<script lang="ts">
	import { ZenoService, type Organization, type User } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import { Icon } from '@smui/button';
	import Button from '@smui/button/src/Button.svelte';
	import Checkbox from '@smui/checkbox/src/Checkbox.svelte';
	import IconButton from '@smui/icon-button/src/IconButton.svelte';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher } from 'svelte';
	import Popup from './Popup.svelte';

	export let organizationToEdit: Organization;
	export let user: User;

	$: members = organizationToEdit.members.sort((a, b) => {
		if (a.id === user.id) return -1;
		else if (b.id === user.id) return 1;
		else if (a.admin && !b.admin) return -1;
		else if (!a.admin && b.admin) return 1;
		return 0;
	});

	const dispatch = createEventDispatcher();

	let input: Textfield;
	let selectedUser: User | undefined;

	$: invalidName = organizationToEdit.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	function updateOrganization() {
		ZenoService.updateOrganization(organizationToEdit).then(() => dispatch('close'));
	}

	function submit(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			dispatch('close');
		}
		if (e.key === 'Enter') {
			updateOrganization();
		}
	}

	function addUser(e: CustomEvent) {
		organizationToEdit.members = [...organizationToEdit.members, { ...e.detail, admin: false }];
		selectedUser = undefined;
	}
</script>

<svelte:window on:keydown={submit} />
<Popup on:close>
	<Content style="display: flex; flex-direction: column;">
		<h2>Organization Aministration</h2>
		<div class="element">
			<Textfield bind:value={organizationToEdit.name} label="Name" bind:this={input} />
		</div>
		<div class="element">
			<h3>Members</h3>
			{#if members.length > 0}
				<table>
					<thead>
						<th style="width: 200px;">Name</th>
						<th>Admin</th>
						<th style="width: auto;" />
					</thead>
					<tbody>
						{#each members as member}
							<tr>
								<td>
									{member.name}
								</td>
								<td>
									<Checkbox
										checked={member.admin}
										on:click={() => (member.admin = !member.admin)}
										disabled={member.id === user.id}
									/>
								</td>
								<td>
									{#if member.id !== user.id}
										<IconButton
											on:click={() => {
												const memberIndex = organizationToEdit.members.findIndex(
													(currentMember) => currentMember.id === member.id
												);
												organizationToEdit.members = [
													...organizationToEdit.members.slice(0, memberIndex),
													...organizationToEdit.members.slice(memberIndex + 1)
												];
											}}
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
							organizationToEdit.members.some((member) => member.id === currentUser.id)
						)
				)}
				{#if availableUsers.length > 0}
					<Svelecte
						style="width: 280px; height: 30px; flex:none; align-self: end; margin-bottom: 20px;"
						bind:value={selectedUser}
						on:change={addUser}
						options={availableUsers}
						placeholder="add members"
						searchable={true}
					/>
				{/if}
			{/await}
		</div>
		<div id="submit">
			<Button style="margin-left: 10px;" variant="outlined" on:click={() => dispatch('close')}
				>Cancel</Button
			>
			<Button
				style="margin-left: 5px;"
				variant="outlined"
				disabled={invalidName}
				on:click={() => updateOrganization()}>{'Update'}</Button
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
