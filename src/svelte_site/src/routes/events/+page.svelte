<script>
  import Events from '../../components/Events.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Events - BTCNews.today';
  });
</script>

<Events events={data.events}/>