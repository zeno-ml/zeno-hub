<script lang="ts">
	export let input: string;
	export let output = false;
</script>

<div class="my-1 flex items-end relative z-0">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 640 512"
		class={`${output ? 'fill-primary' : 'fill-grey-darker'} w-6 mr-2.5 mt-2`}
	>
		<path
			d="M320 0c17.7 0 32 14.3 32 32V96H472c39.8 0 72 32.2 72 72V440c0 39.8-32.2 72-72 72H168c-39.8 0-72-32.2-72-72V168c0-39.8 32.2-72 72-72H288V32c0-17.7 14.3-32 32-32zM208 384c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H208zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H304zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H400zM264 256a40 40 0 1 0 -80 0 40 40 0 1 0 80 0zm152 40a40 40 0 1 0 0-80 40 40 0 1 0 0 80zM48 224H64V416H48c-26.5 0-48-21.5-48-48V272c0-26.5 21.5-48 48-48zm544 0c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H576V224h16z"
		/>
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
