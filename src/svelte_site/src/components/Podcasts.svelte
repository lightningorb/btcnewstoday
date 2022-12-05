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

<Table striped>
  <thead>
    <tr>
      <th width='110px'>Date</th>
      <th>Name</th>
      <th>Episode</th>
    </tr>
  </thead>
  <tbody>
    {#each podcasts as podcast}
      <Podcast podcast={podcast} />
    {/each}
  </tbody>
</Table>