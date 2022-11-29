<script>
  import { Icon } from 'sveltestrap';
  import {API_FQDN} from '$lib/constants.js';
  import axios from 'axios';
  export let podcast;
  export let edit;

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

</script>

<tr>
    <td>{(new Date(podcast.date*1000)).toISOString().slice(0, 10)}</td>
    <td><a target='_blank' href='{podcast.link}'>{podcast.outlet}</a></td>
    <td>{podcast.episode_title}</td>
    {#if edit}
        <button on:click={() => _delete()}><Icon name="trash"/></button>
    {/if}
</tr>
