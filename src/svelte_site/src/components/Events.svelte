<script>
	import { preferences } from '$lib/store.js';
	import { Table, Styles, Icon } from 'sveltestrap';
	import { onMount } from 'svelte';
	import Event from './Event.svelte';
	export let events;
	$: edit = false;
</script>

<div class="section">
	<h2>Events</h2>

	{#if $preferences.access_token != ''}
		{#if !edit}
			<button on:click={() => (edit = true)}><Icon name="pencil-square" /></button>
		{/if}
	{/if}

	<Table striped>
		<thead>
			<tr>
				<th width="110px">Date</th>
				<th>Name</th>
				<th>Location</th>
			</tr>
		</thead>
		<tbody>
			{#each events as event}
				<Event {event} {edit} />
			{/each}
		</tbody>
	</Table>
</div>
