<script lang="ts">
	import { mdiAccount } from '@mdi/js';

	export let input: string;
</script>

<div class="my-2.5 flex items-start">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 448 512"
		class="w-6 mr-2.5 mt-2 fill-grey-darker"
	>
		<path d={mdiAccount} />
	</svg>

	<p class="rounded m-0 p-2.5 border border-grey-darker">{input}</p>
</div>
