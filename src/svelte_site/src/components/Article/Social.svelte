<script>
  import { Input } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  export let article;
  export let edit;
</script>

<Row>
  {#if edit}
      <Input type="textarea" bind:value={article.outlet}/>
  {:else}
    <Col xs="6"><cite><a target='_blank'>{article.outlet}</a></cite></Col>
  {/if}

  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="twitter"/></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="facebook" /></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="link" /></Button></Col>
</Row>