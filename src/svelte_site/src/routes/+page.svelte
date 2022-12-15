<script>
  import Latest from '../components/Latest.svelte';
  import Podcasts from '../components/Podcasts.svelte';
  import { Styles } from 'sveltestrap';
  import { Col, Container, Row } from 'sveltestrap';
  /** @type {import('./$types').PageData} */
  export let data;
  import { page } from '$app/stores';

  let article = null;
  let AID = import.meta.env.VITE_AID;
  let snapshot = import.meta.env.VITE_SNAPSHOT;
  if (AID !== undefined){
    let short = data.articles.filter((x) => x.id == AID)[0];
    let long = data.longforms.filter((x) => x.id == AID)[0];
    article = short || long;
  }
</script>

<!-- {import.meta.env.VITE_PRERENDER} -->

<svelte:head>
{#if article != null}
      <meta name="viewport" content="width=device-width" />
      <meta property="og:url" content={`https://btcnews.today/${snapshot}/${AID}/#${AID}`} />
      <meta property="og:type" content="website" />
      <meta property="og:title" content={article.title} />
      <meta property="og:description" content={article.blurb} />
      <meta property="og:image" content="https://btcnews.today/favicon.png" />
{:else}
      <meta name="viewport" content="width=device-width" />
      <meta property="og:url" content="https://btcnews.today" />
      <meta property="og:type" content="website" />
      <meta property="og:title" content="BTCNews.today" />
      <meta property="og:description" content="Come for the news, stay for the low time preference." />
      <meta property="og:image" content="https://btcnews.today/favicon.png" />
{/if}
</svelte:head>

<Styles />

<Container>
  <Row cols={{ lg: 2, md: 2, sm: 1 }}>
    <Col><Latest slug={data.latest_snapshot} show_dates={false} articles={data.articles} title={'Latest'}/></Col>
    <Col>
      <Row cols={1}>
        <Col><Podcasts podcasts={data.podcasts}/></Col>
        <Col><Latest slug={data.latest_snapshot} articles={data.longforms} title='Longform'/></Col>
      </Row>
    </Col>
  </Row>
</Container>