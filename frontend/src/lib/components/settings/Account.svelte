<script lang="ts">
	import Button from '@smui/button/src/Button.svelte';
	import Textfield from '@smui/textfield';

	export let email: string;
	export let name: string;
</script>

<div class="flex items-center">
	<Textfield label="Username" value={name} disabled style="margin-right: 40px;" />
	<Textfield label="Email" value={email} disabled style="margin-right: 40px;" />
</div>
<div class="mt-5">
	<div class="flex">
		<h5>API Key:</h5>
	</div>
	<Button variant="raised" class="mt-4">Generate new API key</Button>
</div>
