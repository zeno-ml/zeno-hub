<script lang="ts">
	import type { AuthUser } from '$lib/auth/types';
	import Account from '$lib/components/settings/Account.svelte';
	import OrganizationsTable from '$lib/components/settings/OrganizationsTable.svelte';
	import { getEndpoint } from '$lib/util/util';
	import { OpenAPI, type Organization, type User } from '$lib/zenoapi';

	export let data;

	$: user = data.user as User;
	$: cognitoUser = data.cognitoUser as AuthUser;
	$: organizations = data.organizations as Organization[];

	OpenAPI.BASE = `${getEndpoint()}/api`;
</script>

<div class="container">
	<h1>Account management</h1>
	<Account name={cognitoUser.name} email={cognitoUser.email} />
	<OrganizationsTable {organizations} {user} />
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
		margin: 20px;
		width: 100%;
	}
</style>
