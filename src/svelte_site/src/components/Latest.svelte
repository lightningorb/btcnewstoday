<script>
  import { Styles } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { onMount } from "svelte";
  import { Col, Container, Row } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  export let articles;
  export let title;
</script>

<Styles/>

<h1>{title}</h1>

{#each articles as article}
  <Row>
    <Col xs="3"><cite><a target='_blank' href='https://bloomberg.com'>{article.outlet}</a></cite></Col>
    <Col xs="2"><Button secondary><Icon name="twitter" /></Button></Col>
    <Col xs="2"><Button secondary><Icon name="facebook" /></Button></Col>
    <Col xs="2"><Button secondary><Icon name="link" /></Button></Col>
  </Row>

  <td>{(new Date(article.date*1000)).toISOString().slice(0, 10)}</td>

  <h3><a target='_blank' href='{article.link}'>{article.title}</a></h3>

  {article.blurb} …

  <h4>More:</h4> Insider, International Business Times, Reuters, Neowin, Engadget, SlashGear, and The Information

  <h4>Tweets:</h4>
  @caseynewton and @openculture

  <hr/>


{/each}
