<script lang="ts">
	import type { AuthUser } from '$lib/auth/types';
	import Account from '$lib/components/settings/Account.svelte';
	import OrganizationsTable from '$lib/components/settings/OrganizationsTable.svelte';
	import type { Organization, User } from '$lib/zenoapi';

	export let data;

	$: user = data.user as User;
	$: cognitoUser = data.cognitoUser as AuthUser;
	$: organizations = data.organizations as Organization[];
</script>

<div class="flex w-full flex-col bg-yellowish">
	<div class="m-4 flex flex-col rounded bg-white p-6 shadow-md">
		<h1 class="mb-3 text-xl">Account management</h1>
		<Account name={cognitoUser.name} email={cognitoUser.email} />
		<hr class="mt-5 text-grey-lighter" />
		<OrganizationsTable {organizations} {user} />
	</div>
</div>
