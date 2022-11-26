<script>
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";
  export let podcasts;

</script>

<Styles/>

<h2>Podcasts</h2>

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
    <tr>
      <td>{(new Date(podcast.date*1000)).toISOString().slice(0, 10)}</td>
      <td><a target='_blank' href='{podcast.link}'>{podcast.outlet}</a></td>
      <td>{podcast.episode_title}</td>
    </tr>
    {/each}
  </tbody>
</Table>