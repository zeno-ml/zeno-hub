<script lang="ts">
	export let input: string;
	export let output = false;
</script>

<div class="box">
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 640 512"
		class={output ? 'model' : 'no-model'}
	>
		<path
			d="M320 0c17.7 0 32 14.3 32 32V96H472c39.8 0 72 32.2 72 72V440c0 39.8-32.2 72-72 72H168c-39.8 0-72-32.2-72-72V168c0-39.8 32.2-72 72-72H288V32c0-17.7 14.3-32 32-32zM208 384c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H208zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H304zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H400zM264 256a40 40 0 1 0 -80 0 40 40 0 1 0 80 0zm152 40a40 40 0 1 0 0-80 40 40 0 1 0 0 80zM48 224H64V416H48c-26.5 0-48-21.5-48-48V272c0-26.5 21.5-48 48-48zm544 0c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H576V224h16z"
		/>
	</svg>

	<p class="chat message {output ? 'model-border' : 'no-model-border'}">
		{input}
	</p>
</div>

<style>
	.model {
		fill: var(--logo);
	}
	.no-model {
		fill: var(--G3);
	}
	.model-border {
		border: 1px solid var(--logo);
	}
	.no-model-border {
		border: 1px solid rgba(224, 224, 224, 1);
	}
	.box {
		margin-top: 5px;
		margin-bottom: 5px;
		display: flex;
		align-items: end;
		position: relative;
		z-index: 1;
	}
	.box svg {
		min-width: 20px;
		width: 20px;
		margin-right: 10px;
		margin-top: 7px;
	}
	.chat {
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
		left: -7px;
		background-color: rgba(224, 224, 224, 1);
		border-bottom-right-radius: 16px 14px;
		position: absolute;
		bottom: 0;
		height: 25px; /* height of our bubble "tail" - should match the border-radius above */
		content: '';
		z-index: -1;
	}
	.message::after {
		width: 10px;
		background-color: white; /* All tails have the same bg cutout */
		left: -11px;
		border-bottom-right-radius: 10px;
		position: absolute;
		bottom: 0;
		height: 25px; /* height of our bubble "tail" - should match the border-radius above */
		content: '';
		z-index: -1;
	}
	.model-border::before {
		background-color: var(--logo);
	}
</style>
