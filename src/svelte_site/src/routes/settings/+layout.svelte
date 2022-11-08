<script>
  /** @type {import('./$types').LayoutData} */
  export let data;
</script>

<slot></slot>

<h1>Sub-Settings</h1>

<div class="submenu">
  {#each data.sections as section}
    <a href="/settings/{section.slug}">{section.title}</a>
    <br>
  {/each}
</div>

<p>This is the sub-settings page.</p>
