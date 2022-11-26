<script>
  import About from '../../components/About.svelte';
  import { onMount } from 'svelte';
  onMount(() => {
    document.title = 'About - ₿News.daily';
  });
</script>

<About/>