<script lang="ts">
	import type { Project, User, ZenoService } from '$lib/zenoapi';
	import { getContext } from 'svelte';
	import LikeButton from '../general/LikeButton.svelte';

	export let project: Project;
	export let likes: number;
	export let liked: boolean;
	export let user: User | null;

	const zenoClient = getContext('zenoClient') as ZenoService;
</script>

<div class="flex w-full min-w-0 items-center border-b border-b-grey-lighter bg-yellowish-light p-4">
	<h1 class="shrink-0 text-xl font-semibold">{project.name}</h1>
	<p class="overflow-hidden text-ellipsis whitespace-nowrap px-4 pt-1 text-grey-dark">
		{project.description}
	</p>
	<LikeButton on:like={() => zenoClient.likeProject(project.uuid)} {likes} {liked} {user} />
</div>
