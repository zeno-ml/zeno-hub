<script lang="ts">
	import { mdiRobotHappy } from '@mdi/js';

	export let input: string;
	export let output = false;
</script>

<div class="my-1 flex items-end relative z-0">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 640 512"
		class={`${output ? 'fill-primary' : 'fill-grey-darker'} w-6 mr-2.5 mt-2`}
	>
		<path d={mdiRobotHappy} />
	</svg>

	<p
		class="rounded m-0 p-2.5 relative self-start bg-background max-w-[70%]
		before:content-[''] before:-z-[1] before:h-6 before:bottom-0 before:absolute before:rounded-br-2xl before:bg-grey-darker before:w-5 before:-left-2.5
		after:content-[''] after:-z-[1] after:h-6 after:bottom-0 after:absolute after:rounded-br-xl after:bg-background after:w-2.5 after:-left-2.5
		{output ? 'border border-primary before:bg-primary' : 'border border-grey-darker'}"
	>
		{input}
	</p>
</div>
