<script>
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";

  $: events = [];
  let domain = "http://127.0.0.1:8000";

  onMount(async () => {
    if (window.location.hostname == 'btcnews.today'){
      domain = 'https://btcnews.today'
    }

    fetch(domain + '/api/events')
    .then(response => response.json())
    .then(data => {
      events = data;
    }).catch(error => {
      console.log(error);
      return [];
    });
  });

</script>

<Styles/>

<h2>Events</h2>

<Table striped>
  <thead>
    <tr>
      <th>#</th>
      <th>Date</th>
      <th>Name</th>
      <th>Location</th>
    </tr>
  </thead>
  <tbody>
    {#each events as event}
    <tr>
      <th scope="row">1</th>
      <td>{(new Date(event.date*1000)).toISOString().slice(0, 10)}</td>
      <td><a target='_blank' href='{event.link}'>{event.name}</a></td>
      <td>{event.place}</td>
    </tr>
    {/each}
  </tbody>
</Table>