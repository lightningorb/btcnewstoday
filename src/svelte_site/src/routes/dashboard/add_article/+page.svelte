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
        const date = new Date().getTime() / 1000;
        let body = JSON.stringify({
                title,
                blurb,
                link,
                outlet,
                is_longform,
                date
            })
        axios.post('/api/articles/', body, {headers: headers})
          .then(function (response) {
            console.log(response);
            confirm("Looking good");
        })
          .catch(function (error) {
            console.log(error);
            if (error.response != undefined){
                confirm(error.response.data.detail);
            }
            else {
                confirm("Error");
            }
        });
    }
</script>

<FormGroup>
    <Label for="title">Title</Label>
    <br/>
    <Input type="textarea" name="text" id="title" bind:value={title}/>
</FormGroup>

<FormGroup>
    <Label for="blurb">Blurb</Label>
    <br/>
    <Input type="textarea" name="text" id="blurb" bind:value={blurb}/>
</FormGroup>

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

<FormGroup>
    <Input id="c1" type="checkbox" label="Longform" bind:checked={is_longform}/>
</FormGroup>

<br/>

<button type="button" on:click={doPost}>
    Post it.
</button>
