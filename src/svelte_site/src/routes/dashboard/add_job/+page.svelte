<script>
    import { InputGroup, InputGroupText, Input } from 'sveltestrap';
    import { Form, FormGroup, FormText, Label } from 'sveltestrap';
    import axios from 'axios';

    import {API_FQDN} from '$lib/constants.js';
    let link = '';
    let company = '';
    let role = '';
    
    function doPost () {
        const headers = {
            'Content-Type': 'application/json',
        }
        const date = new Date().getTime() / 1000;
        let body = JSON.stringify({
                link,
                company,
                role,
                date
            })
        axios.post('/api/jobs/', body, {headers: headers})
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
    <Label for="company">Company</Label>
    <br/>
    <Input type="textarea" name="text" id="company" bind:value={company}/>
</FormGroup>

<FormGroup>
    <Label for="role">Role</Label>
    <br/>
    <Input type="textarea" name="text" id="role" bind:value={role}/>
</FormGroup>

<br/>

<button type="button" on:click={doPost}>
    Post it.
</button>
