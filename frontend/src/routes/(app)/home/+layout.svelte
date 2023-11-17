<script lang="ts">
	import { page } from '$app/stores';
	import Header from '$lib/components/general/Header.svelte';
	import Help from '$lib/components/general/Help.svelte';
	import NewReportPopup from '$lib/components/popups/NewReportPopup.svelte';

	export let data;
	export let showNewReport = false;

	let isExplore = $page.route.id === '/(app)/home';
</script>

{#if showNewReport && data.user !== null}
	<NewReportPopup on:close={() => (showNewReport = false)} bind:showNewReport />
{/if}

<div class="absolute bottom-6 right-6">
	<Help />
</div>

<div class="flex h-full flex-grow flex-col">
	<Header user={data.user} bind:showNewReport />
	{#if isExplore}
		<div
			class="mx-6 mt-4 flex w-full flex-col items-center justify-center rounded-md bg-primary text-white sm:flex-row"
		>
			<div class="p-6">
				{#if !data.user}
					<h1 class="font-header text-5xl">Welcome to Zeno</h1>
					<p class="text-xl">
						<a class="font-bold hover:text-primary-mid" href="https://zenoml.com"
							>Learn about Zeno</a
						>
						or
						<a class="font-bold hover:text-primary-mid" href="/login">sign in </a>
						or <a class="font-bold hover:text-primary-mid" href="/signup">sign up</a> to create and see
						your projects and reports.
					</p>
				{:else}
					<h1 class="font-header text-4xl">Explore projects and reports</h1>
				{/if}
			</div>

			<div class="ml-auto mr-10">
				<svg
					width="300"
					height="150"
					viewBox="0 0 862 380"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M861.702 424.838L436.864 424.838L436.864 0.000147393L650.895 214.031L861.702 424.838Z"
						fill="#9F55CD"
					>
						<animate attributeName="opacity" values=".6;1;.6" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M417.842 426.106L205.423 213.687L417.842 1.26808L417.842 426.106Z"
						fill="#9F55CD"
						fill-opacity="0.8"
					>
						<animate attributeName="opacity" values=".8;.5;.8" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M392.478 426.106L193.375 426.106L193.375 227.003L392.478 426.106Z"
						fill="#9F55CD"
						fill-opacity="0.6"
					>
						<animate attributeName="opacity" values=".4;.8;.4" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M175.776 425.95L85.1012 335.276L176.255 244.122L175.776 425.95Z"
						fill="#9F55CD"
						fill-opacity="0.5"
					>
						<animate attributeName="opacity" values=".6;.2;.6" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M8.92166e-05 417.575L68.7054 348.87L143.13 423.294L8.92166e-05 417.575Z"
						fill="#9F55CD"
						fill-opacity="0.5"
					>
						<animate attributeName="opacity" values=".2;.4;.2" dur="5s" repeatCount="indefinite" />
					</path>
				</svg>
			</div>
		</div>
	{/if}
	<div class="mx-6 flex min-h-0 flex-col">
		<slot />
	</div>
</div>
