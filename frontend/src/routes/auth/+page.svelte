<script>
	import { goto } from '$app/navigation';
	import Button from '@smui/button/src/Button.svelte';
</script>

<div class="m-auto text-center pt-20 bg-primary h-full">
	<div class="p-10 bg-background w-96 m-auto flex flex-col items-center rounded-md">
		<img src="/zeno.png" alt="zeno logo" class="w-10" />
		<h1 class="mt-4 text-xl font-semibold text-primary">Unauthorized</h1>
		<h1 class="text-xl text-primary">
			The resource you requested cannot be accessed from your account. Please contact the owner to
			share this resource with you.
		</h1>
		<div class="flex">
			<Button on:click={() => history.back()}>Retry</Button>
			<Button on:click={() => goto('/')}>Home</Button>
		</div>
	</div>
</div>
