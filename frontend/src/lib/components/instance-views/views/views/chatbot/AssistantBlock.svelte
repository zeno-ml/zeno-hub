<script lang="ts">
	import { mdiRobotHappy } from '@mdi/js';

	export let input: string;
	export let output = false;
</script>

<div class="my-2.5 flex items-start">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 640 512"
		class={`${output ? 'fill-primary' : 'fill-grey-darker'} w-6 mr-2.5 mt-2`}
	>
		<path d={mdiRobotHappy} />
	</svg>

	<p class="rounded m-0 p-2.5 {output ? 'border border-primary' : 'border border-grey-darker'}">
		{input}
	</p>
</div>
