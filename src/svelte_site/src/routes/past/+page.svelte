<script>
  import Past from '../../components/Past.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Past articles={data.articles} title='Past'/>
