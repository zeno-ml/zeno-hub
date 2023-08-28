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
	$: OpenAPI.HEADERS = {
		Authorization: 'Bearer ' + cognitoUser.accessToken
	};
</script>

<div class="flex flex-col w-full m-5">
	<h1 class="text-xl mb-3">Account management</h1>
	<Account name={cognitoUser.name} email={cognitoUser.email} />
	<hr class="mt-5 text-grey-lighter" />
	<OrganizationsTable {organizations} {user} />
</div>
