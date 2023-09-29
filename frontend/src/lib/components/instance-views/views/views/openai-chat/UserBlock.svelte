<script lang="ts">
	import { mdiAccount } from '@mdi/js';

	export let input: string;
</script>

<div class="my-1 flex justify-end items-end relative z-0">
	<p
		class="border border-grey-darker rounded m-0 p-2.5 relative self-start bg-background max-w-[70%]
		before:content-[''] before:-z-[1] before:h-6 before:bottom-0 before:absolute before:rounded-bl-2xl before:bg-grey-darker before:w-5 before:-right-2.5
		after:content-[''] after:-z-[1] after:h-6 after:bottom-0 after:absolute after:rounded-bl-xl after:bg-background after:w-2.5 after:-right-2.5"
	>
		{input}
	</p>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 448 512"
		class="w-3.5 ml-2.5 mt-2 fill-grey-darker"
	>
		<path d={mdiAccount} />
	</svg>
</div>
