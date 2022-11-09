<script>
  import Podcasts from '../../components/Podcasts.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Podcasts podcasts={data.podcasts}/>