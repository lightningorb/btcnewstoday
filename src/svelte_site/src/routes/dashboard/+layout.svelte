<script>
  /** @type {import('./$types').LayoutData} */
  export let data;
  import { preferences } from '$lib/store.js';
</script>

<slot></slot>

<hr/>

<div class="submenu">
  {#if $preferences.access_token == ''}
    <a href="/dashboard/login">Log in</a>
    <br>
  {/if}
  {#each data.sections as section}
    {#if ((section.auth == true && $preferences.access_token))}
    <a href="/dashboard/{section.slug}">{section.title}</a>
    <br>
    {/if}
  {/each}
</div>

<br>
