<script>
	import Podcast from './Podcast.svelte';
	import { Table, Styles, Icon } from 'sveltestrap';
	import { onMount } from 'svelte';
	export let podcasts;
</script>

<h2>Podcast Drafts</h2>

<Table striped>
	<thead>
		<tr>
			<th width="110px">Date</th>
			<th>Name</th>
			<th>Episode</th>
		</tr>
	</thead>
	<tbody>
		{#each podcasts as podcast}
			<Podcast {podcast} />
		{/each}
	</tbody>
</Table>
