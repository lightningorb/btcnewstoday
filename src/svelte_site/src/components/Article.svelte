<script>
  import { Button } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  export let article;
</script>


<Row>
  <Col xs="6"><cite><a target='_blank' href='https://bloomberg.com'>{article.outlet}</a></cite></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="twitter"/></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="facebook" /></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="link" /></Button></Col>
</Row>

{(new Date(article.date*1000)).toISOString().slice(0, 10)} <span style='font-size: 1.3em;'><a target='_blank' href='{article.link}'>{article.title}</a></span><br/>

<div style='padding-bottom: 10px;'>{article.blurb} …</div>

<div style='padding-bottom: 10px;'><b>More:</b> Insider, International Business Times, Reuters, Neowin, Engadget, SlashGear, and The Information</div>

<div style='padding-bottom: 10px;'><b>Tweets:</b> @caseynewton and @openculture</div>