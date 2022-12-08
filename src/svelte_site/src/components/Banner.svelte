<script>
  import { preferences } from '$lib/store.js';
  import AudioPlayer from './AudioPlayer.svelte';
  import { Styles } from 'sveltestrap';
  import { Col, Container, Row } from 'sveltestrap';
</script>

<Styles/>

<Container>
  <Row cols={1}>
    <Col>
      {#if $preferences.podcast}
        <AudioPlayer src={$preferences.podcast}/>
      {/if}
    </Col>
  </Row>
  <Row cols={1}>
    <Col>
      <h1><a href="https://btcnews.today">BTCNews.Today</a></h1>
      <p>Come for the news, stay for the low time preference.</p>
    </Col>
  </Row>
</Container>


