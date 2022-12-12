<script>
  import { preferences } from '$lib/store.js';
  import { Form, FormGroup, FormText, Label, Input } from 'sveltestrap';
  import { Icon } from 'sveltestrap';
  import {API_FQDN} from '$lib/constants.js';
  import axios from 'axios';
  export let podcast;
  import Play from './Article/Play.svelte';
  let edit = false;

  function _delete(){
    axios.post(`${API_FQDN}/api/delete_podcast/${podcast.id}/`)
      .then(function (response) {
        console.log(response);
        edit = false;
    })
      .catch(function (error) {
        console.log(error);
        confirm("Error");
    });
  }


  function save(){
    const headers = {
        'Content-Type': 'application/json',
    }
    let copy = JSON.parse(JSON.stringify(podcast));
    let body = JSON.stringify(copy)
    axios.post(`${API_FQDN}/api/update_podcast/`, body, {headers: headers})
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

<tr>
    <td>{(new Date(podcast.date*1000)).toISOString().slice(0, 10)}</td>
    {#if edit}
      <td><Input type="text" label="Name" bind:value={podcast.outlet}/></td>
      <td><Input type="text" label="Episode" bind:value={podcast.episode_title}/></td>
    {:else}
      <td><Play podcast={podcast}/><a rel='noreferrer' target='_blank' href='{podcast.link}'>{podcast.outlet}</a></td>
      <td>
        {podcast.episode_title}
        {#if $preferences.access_token != ''}
            <td><button on:click={() => edit=true}><Icon name="pencil-square"/></button></td>
        {/if}
      </td>
    {/if}
</tr>
{#if edit}
  <tr>
      <td><Input type="checkbox" label="Draft" bind:checked={podcast.is_draft}/></td>
      <td><button on:click={() => save()}>Save.</button></td>
      <td><button on:click={() => _delete()}>Delete.</button></td>
  </tr>
{/if}
