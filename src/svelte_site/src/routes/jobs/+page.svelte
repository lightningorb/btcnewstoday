<script>
  import Jobs from '../../components/Jobs.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
</script>

<Jobs jobs={data.jobs}/>