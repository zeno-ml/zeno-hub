<script lang="ts">
	import type { AuthUser } from '$lib/auth/types';
	import Header from '$lib/components/general/Header.svelte';
	import Help from '$lib/components/general/Help.svelte';
	import Account from '$lib/components/settings/Account.svelte';
	import OrganizationsTable from '$lib/components/settings/OrganizationsTable.svelte';
	import type { Organization, User } from '$lib/zenoapi';
	import Button from '@smui/button';

	export let data;

	$: user = data.user as User;
	$: cognitoUser = data.cognitoUser as AuthUser;
	$: organizations = data.organizations as Organization[];

	async function logout() {
		await fetch('/api/logout', { method: 'POST' });
		location.reload();
	}
</script>

<svelte:head>
	<title>Account | Zeno</title>
	<meta name="description" content="Account and organization settings." />
</svelte:head>

<div class="absolute bottom-6 right-6">
	<Help />
</div>

<div class="flex w-full flex-col">
	<Header user={data.user} />
	<div class="mx-6 mb-6 overflow-y-scroll">
		<h1 class="mb-3 mt-2 text-xl">Account management</h1>
		<Account name={cognitoUser.name} email={cognitoUser.email} />
		<hr class="mt-5 text-grey-lighter" />
		<OrganizationsTable {organizations} {user} />
		<div class="mt-2">
			<Button variant="raised" class="mb-2" on:click={logout}>Log Out</Button>
		</div>
	</div>
</div>
