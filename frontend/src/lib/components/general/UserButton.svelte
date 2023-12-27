<script lang="ts">
	import { goto } from '$app/navigation';
	import { tooltip } from '$lib/util/tooltip';
	import type { User } from '$lib/zenoapi';
	import Button from '@smui/button';

	export let user: User | null;
</script>

<div class="flex h-full w-max items-center">
	{#if user}
		<button
			class="h-8 w-8 rounded-full bg-primary font-extrabold capitalize text-white transition hover:bg-primary-mid"
			use:tooltip={{ text: 'My Account' }}
			on:click={() => goto('/account')}
		>
			{user.name.slice(0, 2)}
		</button>
	{:else}
		<div class="h-8">
			<Button class="mr-2 h-full" variant="raised" on:click={() => goto('/signup')}>Sign Up</Button>
			<Button class="h-full" variant="outlined" on:click={() => goto('/login')}>Log In</Button>
		</div>
	{/if}
</div>
