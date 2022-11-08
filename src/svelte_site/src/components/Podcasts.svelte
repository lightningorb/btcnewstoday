<script>
  import { Table, Styles } from 'sveltestrap';
  import { onMount } from "svelte";

  $: podcasts = [];
  let domain = "http://127.0.0.1:8000";

  onMount(async () => {
    if (window.location.hostname == 'btcnews.today'){
      domain = 'https://btcnews.today'
    }

    fetch(domain + '/api/podcasts')
    .then(response => response.json())
    .then(data => {
      podcasts = data;
    }).catch(error => {
      console.log(error);
      return [];
    });
  });

</script>

<Styles/>

<h2>Podcasts</h2>

<Table striped>
  <thead>
    <tr>
      <th>#</th>
      <th>Date</th>
      <th>Name</th>
    </tr>
  </thead>
  <tbody>
    {#each podcasts as podcast}
    <tr>
      <th scope="row">1</th>
      <td>{(new Date(podcast.date*1000)).toISOString().slice(0, 10)}</td>
      <td><a target='_blank' href='{podcast.link}'>{podcast.outlet}</a></td>
    </tr>
    {/each}
  </tbody>
</Table>