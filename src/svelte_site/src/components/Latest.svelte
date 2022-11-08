<script>
  import { Styles } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { onMount } from "svelte";
  import { Col, Container, Row } from 'sveltestrap';
  import { Icon } from 'sveltestrap';

  $: articles = [];
  let domain = "http://127.0.0.1:8000";

  onMount(async () => {
    if (window.location.hostname == 'btcnews.today'){
      domain = 'https://btcnews.today'
    }

    fetch(domain + '/articles')
    .then(response => response.json())
    .then(data => {
      articles = data;
    }).catch(error => {
      console.log(error);
      return [];
    });
  });

</script>

<Styles/>

<h1>Latest</h1>

{#each articles as article}
  <Row>
    <Col xs="3"><cite><a href='https://bloomberg.com'>{article.outlet}</a></cite></Col>
    <Col xs="2"><Button secondary><Icon name="twitter" /></Button></Col>
    <Col xs="2"><Button secondary><Icon name="facebook" /></Button></Col>
    <Col xs="2"><Button secondary><Icon name="link" /></Button></Col>
  </Row>

  <h3><a href='{article.link}'>{article.title}</a></h3>

  {article.blurb} …

  <h4>More:</h4> Insider, International Business Times, Reuters, Neowin, Engadget, SlashGear, and The Information

  <h4>Tweets:</h4>
  @caseynewton and @openculture

  <hr/>


{/each}
