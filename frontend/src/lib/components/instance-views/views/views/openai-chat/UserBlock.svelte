<script lang="ts">
	export let input: string;
</script>

<div class="box">
	<p class="chat message">{input}</p>
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
		<path
			d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"
		/>
	</svg>
</div>

<style>
	.box {
		margin-top: 5px;
		margin-bottom: 5px;
		display: flex;
		justify-content: end;
		align-items: end;
		position: relative;
		z-index: 1;
	}
	.box svg {
		min-width: 15px;
		width: 15px;
		margin-left: 10px;
		margin-top: 7px;
		fill: var(--G3);
	}
	.chat {
		border: 1px solid rgba(224, 224, 224, 1);
		border-radius: 5px;
		margin: 0px;
		padding: 10px;
		overflow-wrap: anywhere;
		max-width: 70%;
	}
	.message {
		position: relative; /* Setup a relative container for our psuedo elements */
		word-wrap: break-word; /* Make sure the text wraps to multiple lines if long */
		align-self: flex-start;
		background-color: white;
	}
	.message::before {
		width: 20px;
		right: -7px;
		background-color: rgba(224, 224, 224, 1);
		border-bottom-left-radius: 16px 14px;
		position: absolute;
		bottom: 0;
		height: 25px; /* height of our bubble "tail" - should match the border-radius above */
		content: '';
		z-index: -1;
	}
	.message::after {
		width: 10px;
		background-color: white; /* All tails have the same bg cutout */
		right: -11px;
		border-bottom-left-radius: 10px;
		position: absolute;
		bottom: 0;
		height: 25px; /* height of our bubble "tail" - should match the border-radius above */
		content: '';
		z-index: -1;
	}
</style>
