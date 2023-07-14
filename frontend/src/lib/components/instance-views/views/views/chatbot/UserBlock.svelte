<script>
	export let input;
</script>

<div class="box">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
		<path
			d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"
		/>
	</svg>

	<p class="chat">{input}</p>
</div>

<style>
	.box {
		margin-top: 10px;
		margin-bottom: 10px;
		display: flex;
		align-items: start;
	}
	.box svg {
		min-width: 24px;
		width: 24px;
		margin-right: 10px;
		margin-top: 7px;
		fill: var(--G3);
	}
	.chat {
		border: 1px solid rgba(224, 224, 224, 1);
		border-radius: 5px;
		margin: 0px;
		padding: 10px;
		overflow-wrap: anywhere;
	}
</style>
