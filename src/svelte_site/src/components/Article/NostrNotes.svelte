<script>
  import { Popover } from 'sveltestrap';
  export let article;
  article.nostr_notes.sort((a, b) => a.id - b.id);
</script>

<div>

{#if article.nostr_notes.length > 0}
  <b class='tweets-title'>Nostr:</b>
{/if}

{#each article.nostr_notes as nostr_note}
  <Popover
    trigger="hover"
    target={'id-'+nostr_note.note_id}
    title={'@'+nostr_note.username}
  >
    <p>{nostr_note.text}</p>
  </Popover>
  <a rel="noreferrer" class='tweet' id={'id-'+nostr_note.note_id} target='_blank' href="https://astral.ninja/event/{nostr_note.note_id}">@{nostr_note.username}</a> <span style='width: 3px;'></span>
{/each}
</div>