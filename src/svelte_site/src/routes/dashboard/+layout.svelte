<script>
  /** @type {import('./$types').LayoutData} */
  export let data;
</script>

<slot></slot>

<hr/>

<div class="submenu">
  {#each data.sections as section}
    <a href="/dashboard/{section.slug}">{section.title}</a>
    <br>
  {/each}
</div>

<br>
