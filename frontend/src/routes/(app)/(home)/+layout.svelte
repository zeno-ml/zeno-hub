<script lang="ts">
	import { page } from '$app/stores';
	import Banner from '$lib/components/general/Banner.svelte';
	import HomeHeader from '$lib/components/general/HomeHeader.svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let data;

	let isExplore =
		$page.route.id === '/(app)/(home)/reports' || $page.route.id === '/(app)/(home)/projects';
</script>

<div class="flex flex-col w-full h-full p-6 pt-5 bg-white">
	{#if data.cognitoUser && data.cognitoUser !== null}
		<div class="flex text-3xl">
			<Tooltip content={'Your projects and reports'} theme={'zeno-tooltip'} position="bottom">
				<a
					href={'/' + data.cognitoUser.name + '/projects'}
					class={`mr-6 ${isExplore ? 'text-grey-dark' : ''} hover:text-primary`}
				>
					My Hub
				</a>
			</Tooltip>
			<Tooltip content={'Public projects and reports'} theme={'zeno-tooltip'} position="bottom">
				<a href="/projects" class={`${!isExplore ? 'text-grey-dark' : ''} hover:text-primary`}>
					Discover
				</a>
			</Tooltip>
		</div>
	{:else}
		<Banner
			>Welcome to <a class="text-primary font-medium" href="https://zenoml.com">Zeno</a>!
			<a class="text-primary font-medium" href="/login">Sign in </a>
			or <a class="text-primary font-medium" href="/signup">sign up</a> to create and see your projects
			and reports.</Banner
		>
	{/if}
	<div class="mt-8 flex flex-col">
		<HomeHeader user={isExplore ? '' : data.cognitoUser?.name} />
		<slot />
	</div>
</div>
