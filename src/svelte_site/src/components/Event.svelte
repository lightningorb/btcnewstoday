<script>
  import { Icon } from 'sveltestrap';
  import {API_FQDN} from '$lib/constants.js';
  import axios from 'axios';
  export let event;
  export let edit;

  function _delete(){
    axios.post(`${API_FQDN}/api/delete_event/${event.id}/`)
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
  <td>{(new Date(event.date*1000)).toISOString().slice(0, 10)}</td>
  <td><a target='_blank' href='{event.link}'>{event.name}</a></td>
  <td>{event.place}</td>
  {#if edit}
    <button on:click={() => _delete()}><Icon name="trash"/></button>
  {/if}
</tr>