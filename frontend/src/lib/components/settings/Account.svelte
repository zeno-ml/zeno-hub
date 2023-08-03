<script lang="ts">
	import Textfield from '@smui/textfield';

	export let email: string;
	export let name: string;
</script>

<div class="flex items-center">
	<Textfield label="Username" value={name} disabled style="margin-right: 40px;" />
	<Textfield label="Email" value={email} disabled style="margin-right: 40px;" />
</div>
