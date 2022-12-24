<script lang="ts">
  import { API_FQDN } from "$lib/constants.js"
  import { InputGroup, InputGroupText, Input, Icon } from 'sveltestrap';
  import { Form, FormGroup, FormText, Label } from 'sveltestrap';
  import axios from 'axios';  import { Button, Modal } from 'sveltestrap';
  import { Card, CardBody } from 'sveltestrap';
  
  let open = false;
  let link = '';

  export var article_id;

  function tweet_re(link){
      var rx = /https:\/\/twitter\.com\/(.*)\/status\/([0-9]*)/g;
      var arr = rx.exec(link);
      if (arr != null && arr.length == 3)
        var doc = {username: arr[1], id: arr[2]};
        return doc
  }

  async function get_tweet(uid){
    if (uid == null)
      return
    const res = await fetch(API_FQDN+`/api/third_party/tweet_text/?tweet_id=${uid.id}`);
    const text = await res.json();
    return text;
  }

  function add_tweet(username, id, text){
    const headers = {
        'Content-Type': 'application/json',
    }
    let body = JSON.stringify({
            username,
            text,
            article_id,
            id,
        })
    axios.post('/api/tweets/', body, {headers: headers})
      .then(function (response) {
        console.log(response);
        confirm("Looking good");
    })
      .catch(function (error) {
        console.log(error);
        confirm("Error");
    });    
  }

  $: uid = tweet_re(link);
  $: tweet = get_tweet(uid);

  const toggle = () => (open = !open);
</script>

<div>
  <Button size="sm" on:click={toggle}><Icon name='twitter' /></Button>

  <Modal body header="Add Tweet" isOpen={open} {toggle}>
    <FormGroup>
    <Label for="link">Tweet link:</Label>
    <br/>
    <Input type="textarea" name="text" id="link" bind:value={link}/>
    <br/>
    {#if uid}
      Username: {uid.username}
      <br/>
      ID: {uid.id}
      <br/>
      {#await tweet}
        <p>fetching tweet...</p>
      {:then text}
        <Card>
          <CardBody>{text}</CardBody>
        </Card>
          <Button color="danger" on:click={() => add_tweet(uid.username, uid.id, text)} size="sm">Add Tweet</Button>
      {/await}
      <br/>
    {/if}
</FormGroup>

  </Modal>
</div>