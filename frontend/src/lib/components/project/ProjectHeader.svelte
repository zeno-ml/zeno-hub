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

<div class="flex p-4 bg-yellowish-light border-b border-b-grey-lighter">
	<div class="flex flex-col">
		<h1 class="text-xl font-semibold">{project.name}</h1>
		<p>{project.description}</p>
	</div>
	<LikeButton on:like={() => zenoClient.likeProject(project.uuid)} {likes} {liked} {user} />
</div>
