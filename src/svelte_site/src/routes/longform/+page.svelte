<script>
  import Latest from '../../components/Latest.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Latest articles={data.articles} title='Longform'/>