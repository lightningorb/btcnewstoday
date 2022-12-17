<script>
  import { onMount } from 'svelte';
  import { browser, dev } from '$app/environment';
  // import { PUBLIC_BASE_URL } from '$env/static/public';
  onMount(() => {
    document.title = 'Dashboard - BTCNews.today';
  });
</script>



<h1>Debug</h1>

<p>Some useful information whilst developing.</p>

<p>Browser: {browser}</p>
<!-- <p>Building: {building}</p> -->
<p>Dev: {dev}</p>
<!-- <p>Version: {version}</p> -->
<!-- <p>PUBLIC_BASE_URL: {PUBLIC_BASE_URL}</p> -->