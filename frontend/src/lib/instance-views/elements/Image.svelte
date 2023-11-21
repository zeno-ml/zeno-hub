<script lang="ts">
	import type { Image } from '$lib/instance-views/schema.js';
	import { mdiArrowExpand, mdiClose } from '@mdi/js';

	export let data: string;
	export let spec: Image;

	const widthMap = {
		small: 'w-48',
		medium: 'w-64',
		large: 'w-96',
		full: 'w-full'
	};

	let showPopup = false;
</script>

<div class="group relative">
	<img
		class={spec.maxWidth ? widthMap[spec.maxWidth] : ''}
		src={data}
		alt="Image thumbnail for instance {data}"
	/>
	<button
		class="absolute right-0 top-0 hidden rounded-md p-1 hover:bg-primary-ligther group-hover:inline"
		on:click={(e) => {
			showPopup = true;
			e.preventDefault();
		}}
	>
		<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
			<path d={mdiArrowExpand} />
		</svg>
	</button>
</div>

{#if showPopup}
	<div
		id="fullscreenModal"
		class="bg-gray-500 fixed inset-0 z-50 flex items-center justify-center bg-opacity-75 p-4"
	>
		<div class="relative w-full max-w-2xl rounded-lg bg-white p-6 shadow-xl">
			<button
				on:click={() => (showPopup = false)}
				class="absolute right-0 top-0 mr-4 mt-4 rounded-md p-1 hover:bg-primary-ligther"
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-6 fill-grey-darker">
					<path d={mdiClose} />
				</svg>
			</button>
			<img src={data} alt="Image thumbnail for instance {data}" />
		</div>
	</div>
{/if}
