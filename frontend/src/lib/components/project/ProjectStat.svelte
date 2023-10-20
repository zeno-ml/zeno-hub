<script lang="ts">
	import { shortenNumber } from '$lib/util/util';
	import { Icon } from '@smui/button';

	export let icon: string;
	export let text: string | number;
</script>

<div class="flex items-center mr-8">
	<div class="w-6 h-6 fill-grey-dark mr-2">
		<Icon style="outline:none" tag="svg" viewBox="0 0 24 24">
			<path d={icon} />
		</Icon>
	</div>
	{typeof text === 'number' ? shortenNumber(text, 1) : text}
</div>
