<script>
	import Note from './Note.svelte';
    import { role_is_at_least } from '$lib/utils.js';
	export let article;
	article.nostr_notes.sort((a, b) => a.id - b.id);
	var notes = role_is_at_least('editor') ? article.nostr_notes : article.nostr_notes.filter((a) => a.approved);
	let display = notes.length;
</script>

{#if display}
<div style="padding-top: 10px;">
	{#if notes.length > 0}
		<b class="tweets-title">Nostr:</b>
	{/if}

	{#each notes as note}
		<Note note={note}/>
	{/each}
</div>
{/if}