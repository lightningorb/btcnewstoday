<script>
  import Jobs from '../../components/Jobs.svelte';
  /** @type {import('./$types').PageData} */
  export let data;
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'Jobs - ₿News.daily';
  });
</script>

<Jobs jobs={data.jobs}/>