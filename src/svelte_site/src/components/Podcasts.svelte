<script>
  import { preferences } from '$lib/store.js';
  import { Table, Styles, Icon } from 'sveltestrap';
  import { onMount } from "svelte";
  import Podcast from './Podcast.svelte';
  export let podcasts;
  $: edit = false;

</script>

<Styles/>

<h2>Podcasts</h2>

{#if $preferences.access_token != ''}
  {#if edit}
  {:else}
    <button on:click={() => edit=true}><Icon name="pencil-square"/></button>
  {/if}
{/if}

<Table striped>
  <thead>
    <tr>
      <th>Date</th>
      <th>Name</th>
      <th>Episode</th>
    </tr>
  </thead>
  <tbody>
    {#each podcasts as podcast}
      <Podcast podcast={podcast} edit={edit} />
    {/each}
  </tbody>
</Table>