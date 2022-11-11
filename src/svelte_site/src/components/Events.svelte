<script>
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";
  export let events;
</script>

<Styles/>

<h2>Events</h2>

<Table striped>
  <thead>
    <tr>
      <th>Date</th>
      <th>Name</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    {#each events as event}
    <tr>
      <td>{(new Date(event.date*1000)).toISOString().slice(0, 10)}</td>
      <td><a target='_blank' href='{event.link}'>{event.name}</a></td>
      <td>{event.place}</td>
    </tr>
    {/each}
  </tbody>
</Table>