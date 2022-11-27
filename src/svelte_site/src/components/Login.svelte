<script lang="ts">
  import { InputGroup, InputGroupText, Input } from 'sveltestrap';
  import axios from 'axios';
  import { API_FQDN } from "$lib/constants.js"

  import { get } from 'svelte/store'
  import { preferences } from '$lib/store.js';

  let username = '';
  let password = '';

  function login(){
    const headers = {
        'Content-Type': 'application/json',
    }
    var bodyFormData = new FormData();
    bodyFormData.append('username', username);
    bodyFormData.append('password', password); 
    const request = {
      method: 'post',
      url: `${API_FQDN}/token/`,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" }
    }

    axios(request)
    .then((response) => {
        console.log(response);
        preferences.set({access_token: response.data.access_token});
    })
    .catch((error) => {
        console.log(error);
        confirm("Error");
    });
  }

</script>

<h1>Login</h1>

<InputGroup>
<table width='300px'>
  <tr>
    <td>
      <InputGroupText>username</InputGroupText>
    </td>
    <td>
      <Input placeholder="username" bind:value={username}/>
    </td>
  </tr>
  <tr>
    <td>
      <InputGroupText>password</InputGroupText>
    </td>
    <td>
      <Input placeholder="password" bind:value={password}/>
    </td>
  </tr>
</table>
</InputGroup>

<br />

<button on:click={login}>Log in</button>


<h1>Register</h1>

<InputGroup>
<table width='300px'>
  <tr>
    <td>
      <InputGroupText>username</InputGroupText>
    </td>
    <td>
      <Input placeholder="username" />
    </td>
  </tr>
  <tr>
    <td>
      <InputGroupText>password</InputGroupText>
    </td>
    <td>
      <Input placeholder="password" />
    </td>
  </tr>
</table>
</InputGroup>

<br />

<button>Register</button>

<br />
<br />
