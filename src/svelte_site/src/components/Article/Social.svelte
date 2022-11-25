<script>
  import { Icon } from 'sveltestrap';
  import { Button } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  export let article;
</script>

<Row>
  <Col xs="6"><cite><a target='_blank' href='https://bloomberg.com'>{article.outlet}</a></cite></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="twitter"/></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="facebook" /></Button></Col>
  <Col xs="2"><Button secondary size="sm" class='show-on-hover'><Icon name="link" /></Button></Col>
</Row>