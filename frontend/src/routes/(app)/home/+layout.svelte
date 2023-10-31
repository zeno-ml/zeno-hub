<script lang="ts">
	import { page } from '$app/stores';
	import { Tooltip } from '@svelte-plugins/tooltips';

	export let data;

	let isExplore = $page.route.id === '/(app)/home';
	let loggedIn = data.cognitoUser && data.cognitoUser !== null;
</script>

<div class="flex flex-col w-full h-full p-8 pt-5 bg-white">
	<div
		class="bg-[#9F55CD] w-full rounded-md text-white flex justify-center items-center flex-col sm:flex-row p-6 sm:h-40"
	>
		{#if loggedIn}
			<div class="flex text-3xl">
				<Tooltip content={'Your projects and reports'} theme={'zeno-tooltip'} position="bottom">
					<a
						href={'/home/' + data.cognitoUser?.name}
						class={`mr-6 ${
							isExplore ? 'text-grey-lighter no-underline' : ''
						} hover:text-primary uppercase font-bold underline`}
					>
						My Hub
					</a>
				</Tooltip>
				<Tooltip content={'Public projects and reports'} theme={'zeno-tooltip'} position="bottom">
					<a
						href="/home"
						class={`${
							!isExplore ? 'text-grey-lighter no-underline' : ''
						} hover:text-primary uppercase font-bold underline`}
					>
						Discover
					</a>
				</Tooltip>
			</div>
		{:else}
			<div>
				<h1 class="text-5xl font-header">Welcome to Zeno</h1>
				<p class="text-xl">
					<a class="font-bold hover:text-primary" href="/login">Sign in </a>
					or <a class="font-bold hover:text-primary" href="/signup">sign up</a> to create and see your
					projects and reports.
				</p>
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
						fill="#612593"
					>
						<animate attributeName="opacity" values=".6;1;.6" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M417.842 426.106L205.423 213.687L417.842 1.26808L417.842 426.106Z"
						fill="#612593"
						fill-opacity="0.8"
					>
						<animate attributeName="opacity" values=".8;.5;.8" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M392.478 426.106L193.375 426.106L193.375 227.003L392.478 426.106Z"
						fill="#612593"
						fill-opacity="0.6"
					>
						<animate attributeName="opacity" values=".4;.8;.4" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M175.776 425.95L85.1012 335.276L176.255 244.122L175.776 425.95Z"
						fill="#612593"
						fill-opacity="0.5"
					>
						<animate attributeName="opacity" values=".6;.2;.6" dur="5s" repeatCount="indefinite" />
					</path>
					<path
						d="M8.92166e-05 417.575L68.7054 348.87L143.13 423.294L8.92166e-05 417.575Z"
						fill="#612593"
						fill-opacity="0.5"
					>
						<animate attributeName="opacity" values=".2;.4;.2" dur="5s" repeatCount="indefinite" />
					</path>
				</svg>
			</div>
		{/if}
	</div>
	<div class="mt-6 flex flex-col min-h-0">
		<slot />
	</div>
</div>
