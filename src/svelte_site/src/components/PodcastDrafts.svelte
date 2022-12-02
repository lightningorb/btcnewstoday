<script>
  import Podcast from './Podcast.svelte';
  import { Styles } from 'sveltestrap';
  import { onMount } from "svelte";
  export let podcasts;
</script>

<Styles/>

<h2>Podcast Drafts</h2>

{#each podcasts as podcast}
  <Podcast podcast={podcast}/>
  <br/>
  <hr/>
{/each}
