<script>
  import Events from '../../components/Events.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Events events={data.events}/>