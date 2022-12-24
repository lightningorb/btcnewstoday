<script>
  import { preferences } from '$lib/store.js';
  import axios from 'axios';
  import AddTweet from './AddTweet.svelte';
  import AddNostrNote from './AddNostrNote.svelte';
  import Blurb from './Blurb.svelte';
  import Title from './Title.svelte';
  import { Form, FormGroup, FormText, Label } from 'sveltestrap';
  import Tweets from './Tweets.svelte';
  import NostrNotes from './NostrNotes.svelte';
  import Social from './Social.svelte';
  import More from './More.svelte';
  import { Button } from 'sveltestrap';
  import { Popover } from 'sveltestrap';
  import { Input, Icon } from 'sveltestrap';
  import {API_FQDN} from '$lib/constants.js';
  import { Col, Container, Row } from 'sveltestrap';
  export let slug;
  export let article;
  export let show_dates = false;
  $: edit = false;

  function save(){
    console.log(article)
    const headers = {
        'Content-Type': 'application/json',
    }
    let copy = JSON.parse(JSON.stringify(article));
    delete copy.tweets;
    delete copy.id;
    let body = JSON.stringify(copy)
    axios.post(`${API_FQDN}/api/update_article/${article.id}/`, body, {headers: headers})
      .then(function (response) {
        console.log(response);
        edit = false;
    })
      .catch(function (error) {
        console.log(error);
        confirm("Error");
    });
  }

  function _delete(){
    axios.post(`${API_FQDN}/api/delete_article/${article.id}/`)
      .then(function (response) {
        console.log(response);
        edit = false;
    })
      .catch(function (error) {
        console.log(error);
        confirm("Error");
    });
  }

</script>

<div id={article.id}></div>

<div class="container">
  <div class="row">
    <div class="col-lg-12 pt-4 pt-lg-0">
      <!-- <span>{(new Date(article.date*1000)).toISOString()}</span> -->
      <Social article={article} edit={edit} slug={slug}/>
        {#if $preferences.show_images}
          <img src={article.image} class="article-hero-image float-end imgshadow" alt="">
        {/if}
      <Title article={article} edit={edit} show_dates={show_dates}/>
    <Blurb article={article} edit={edit}/>
    <NostrNotes article={article}/>
    <Tweets article={article}/>
    </div>
    <div style="text-align: left;" class="col-lg-5">
    </div>
  </div>
</div>

{#if edit}
  <FormGroup>
      <Input id="c1" type="checkbox" label="Longform" bind:checked={article.is_longform}/>
      <Input id="c2" type="checkbox" label="Draft" bind:checked={article.is_draft}/>
  </FormGroup>
  <button on:click={() => save()}>Save.</button>
  <button on:click={() => _delete()}>Delete.</button>
{:else}
  {#if $preferences.access_token != ''}
    <Row>
      <Col xs='2'>
        <button on:click={() => edit=true}><Icon name="pencil-square"/></button>
      </Col>
      <Col xs='2'>
        <AddTweet article_id={article.id}/><br/>
        <AddNostrNote article_id={article.id}/><br/>
      </Col>
    </Row>
  {/if}
{/if}