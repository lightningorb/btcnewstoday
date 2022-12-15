<script>
  import { preferences } from '$lib/store.js';
  import { Input } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  import { browser, dev } from '$app/environment';
  export let slug;
  export let article;
  export let edit;
  let perm;
  perm = `/${slug}/${article.id}#${article.id}`
</script>

<Row>
  {#if edit}
      <Input type="textarea" bind:value={article.outlet}/>
  {:else}
    <Col xs="6"><cite><a href={null} target='_blank' rel="noreferrer" on:click|preventDefault>{article.outlet}</a></cite></Col>
  {/if}
  {#if browser}
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="twitter"/></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="facebook" /></Button></Col>
  <Col xs="2"><a href={perm}><Button secondary size="sm" class='show-on-hover'><Icon name="link" /></Button></a></Col>
  {/if}
</Row>