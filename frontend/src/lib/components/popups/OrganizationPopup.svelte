<script lang="ts">
	import type { Organization, User, ZenoService } from '$lib/zenoapi';
	import { mdiClose } from '@mdi/js';
	import Button, { Icon } from '@smui/button';
	import Checkbox from '@smui/checkbox';
	import IconButton from '@smui/icon-button';
	import { Content } from '@smui/paper';
	import Textfield from '@smui/textfield';
	import Svelecte from 'svelecte';
	import { createEventDispatcher, getContext } from 'svelte';
	import Popup from './Popup.svelte';

	export let organizationToEdit: Organization;
	export let user: User;

	const dispatch = createEventDispatcher();
	const zenoClient = getContext('zenoClient') as ZenoService;

	let input: Textfield;
	let selectedUser: User | undefined;

	$: members = organizationToEdit.members.sort((a, b) => {
		if (a.id === user.id) return -1;
		else if (b.id === user.id) return 1;
		else if (a.admin && !b.admin) return -1;
		else if (!a.admin && b.admin) return 1;
		return 0;
	});

	$: invalidName = organizationToEdit.name.length === 0;
	$: if (input) {
		input.getElement().focus();
	}

	function updateOrganization() {
		zenoClient.updateOrganization(organizationToEdit).then(() => dispatch('close'));
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
	<Content class="flex flex-col">
		<h2>Organization Settings</h2>
		<div class="mb-5 flex flex-col">
			<Textfield bind:value={organizationToEdit.name} label="Name" bind:this={input} />
		</div>
		<div class="mb-5 flex flex-col">
			<h3>Members</h3>
			{#if members.length > 0}
				<table>
					<thead
						class="sticky left-0 top-0 border-b border-grey-lighter bg-background pb-1 font-semibold"
					>
						<th class="w-[200px]">Email</th>
						<th>Admin</th>
						<th class="w-auto" />
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
			{#await zenoClient.getUsers() then users}
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
		<div class="flex items-center self-end">
			<Button class="ml-4" variant="outlined" on:click={() => dispatch('close')}>Cancel</Button>
			<Button
				class="ml-2"
				variant="outlined"
				disabled={invalidName}
				on:click={() => updateOrganization()}>{'Update'}</Button
			>
		</div>
	</Content>
</Popup>
