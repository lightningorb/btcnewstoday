<script>
  import { preferences } from '$lib/store.js';
  import axios from 'axios';
  import AddTweet from './AddTweet.svelte';
  import Blurb from './Blurb.svelte';
  import Title from './Title.svelte';
  import { Form, FormGroup, FormText, Label } from 'sveltestrap';
  import Tweets from './Tweets.svelte';
  import Social from './Social.svelte';
  import More from './More.svelte';
  import { Button } from 'sveltestrap';
  import { Popover } from 'sveltestrap';
  import { Input, Icon } from 'sveltestrap';
  import { Col, Row } from 'sveltestrap';
  import {API_FQDN} from '$lib/constants.js';
  export let article;
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

<Social article={article}/>
<Title article={article} edit={edit}/>
<Blurb article={article} edit={edit}/>
<!-- <More article={article}/> -->
<Tweets article={article} edit={edit}/>

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
      </Col>
    </Row>
  {/if}
{/if}