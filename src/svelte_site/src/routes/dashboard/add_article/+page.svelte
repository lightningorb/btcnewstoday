<script>
    import { InputGroup, InputGroupText, Input } from 'sveltestrap';
    import { Form, FormGroup, FormText, Label } from 'sveltestrap';
    import axios from 'axios';

    import {API_FQDN} from '$lib/constants.js';
    let title = '';
    let blurb = '';
    let link = '';
    let outlet = '';
    let is_longform = false;
    
    function doPost () {
        const headers = {
            'Content-Type': 'application/json',
        }
        let body = JSON.stringify({
                title,
                blurb,
                link,
                outlet,
                is_longform
            })
        axios.post('/api/articles/', body, {headers: headers})
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
    <Label for="exampleText">Title</Label>
    <br/>
    <Input type="textarea" name="text" id="exampleText" bind:value={title}/>
</FormGroup>

<FormGroup>
    <Label for="exampleText">Blurb</Label>
    <br/>
    <Input type="textarea" name="text" id="exampleText" bind:value={blurb}/>
</FormGroup>

<FormGroup>
    <Label for="exampleText">Link</Label>
    <br/>
    <Input type="textarea" name="text" id="exampleText" bind:value={link}/>
</FormGroup>

<FormGroup>
    <Label for="exampleText">Outlet</Label>
    <br/>
    <Input type="textarea" name="text" id="exampleText" bind:value={outlet}/>
</FormGroup>

<button type="button" on:click={doPost}>
    Post it.
</button>
