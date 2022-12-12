<script>
  import { preferences } from '$lib/store.js';
  import { Input } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  export let slug;
  export let article;
  export let edit;
  let perm;
  if (slug == undefined){
    let date = new Date();
    let dateString = date.toUTCString();
    let formattedDateString = date.toISOString().slice(0, 10);
    perm = `/templink/${formattedDateString}:${article.id}?#${article.id}`
  } else {
    perm = `/templink/${slug}?#${article.id}`
  }
</script>

<Row>
  {#if edit}
      <Input type="textarea" bind:value={article.outlet}/>
  {:else}
    <Col xs="6"><cite><a target='_blank'>{article.outlet}</a></cite></Col>
  {/if}

  {#if $preferences.access_token != ''}
    <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="twitter"/></Button></Col>
    <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="facebook" /></Button></Col>
    <Col xs="2"><a href={perm}><Button secondary size="sm" class='show-on-hover'><Icon name="link" /></Button></a></Col>
  {/if}
</Row>