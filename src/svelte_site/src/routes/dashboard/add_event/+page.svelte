<script>
    import { InputGroup, InputGroupText, Input } from 'sveltestrap';
    import { Form, FormGroup, FormText, Label } from 'sveltestrap';
    import axios from 'axios';

    import {API_FQDN} from '$lib/constants.js';
    let link = '';
    let name = '';
    let place = '';
    let date = '';
    
    function doPost () {
        const headers = {
            'Content-Type': 'application/json',
        }
        date = Date.parse(date) / 1000;
        console.log('date', date)
        let body = JSON.stringify({
                link,
                name,
                place,
                date
            })
        axios.post('/api/events/', body, {headers: headers})
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
    <Label for="name">Name</Label>
    <br/>
    <Input type="textarea" name="text" id="name" bind:value={name}/>
</FormGroup>

<FormGroup>
    <Label for="place">Place</Label>
    <br/>
    <Input type="textarea" name="text" id="place" bind:value={place}/>
</FormGroup>

<FormGroup>
    <Label for="exampleDate">Date</Label>
    <Input
      type="date"
      name="date"
      id="exampleDate"
      placeholder="date placeholder"
      bind:value={date}
    />
</FormGroup>

<br/>

<button type="button" on:click={doPost}>
    Post it.
</button>
