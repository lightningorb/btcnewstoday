<script>
    import { InputGroup, InputGroupText, Input } from 'sveltestrap';
    import { Form, FormGroup, FormText, Label } from 'sveltestrap';
    import axios from 'axios';

    import {API_FQDN} from '$lib/constants.js';
    let link = '';
    let outlet = '';
    
    function doPost () {
        const headers = {
            'Content-Type': 'application/json',
        }
        const date = new Date().getTime() / 1000;
        let body = JSON.stringify({
                link,
                outlet,
                date
            })
        axios.post('/api/podcasts/', body, {headers: headers})
          .then(function (response) {
            console.log(response);
            confirm("Looking good");
        })
          .catch(function (error) {
            console.log(error);
            confirm("Error");
        });
    }
</script>

<FormGroup>
    <Label for="link">Link</Label>
    <br/>
    <Input type="textarea" name="text" id="link" bind:value={link}/>
</FormGroup>

<FormGroup>
    <Label for="outlets">Outlet</Label>
    <br/>
    <Input type="textarea" name="text" id="outlets" bind:value={outlet}/>
</FormGroup>

<br/>

<button type="button" on:click={doPost}>
    Post it.
</button>
