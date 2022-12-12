<script>
  import PodcastDrafts from '../../../components/PodcastDrafts.svelte';

  /** @type {import('./$types').PageData} */
  export let data;
</script>

<PodcastDrafts podcasts={data.podcasts}/>
