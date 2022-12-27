<script type="text/javascript">
    import { role_is_at_least } from '$lib/utils.js';
    import { Input, Icon } from 'sveltestrap';
    import { Popover } from 'sveltestrap';
    import { Col, Container, Row } from 'sveltestrap';
    import AddTweet from './AddTweet.svelte';
    import AddNostrNote from './AddNostrNote.svelte';
    export let article;
    export let edit;
    let is_contribute_open = false;
    function on_click(){
        edit = true;
        is_contribute_open = false;
    }
</script>

<Icon id={`btn-right-${article.id}`} style="padding-left: 5px; font-size: 0.8em;" name="plus-circle" />
<Popover bind:is_contribute_open target={`btn-right-${article.id}`} style='width: 150px;' placement='bottom'> 
    <Row>
        {#if role_is_at_least('editor')}
            <div><button style='border: 0;' on:click={on_click}><Icon name="pencil-square" /></button> Edit</div>
        {/if}
        {#if role_is_at_least('contributor')}
            <AddTweet article_id={article.id} bind:is_contribute_open={is_contribute_open}/><br />
            <AddNostrNote article_id={article.id} bind:is_contribute_open={is_contribute_open}/><br />
        {/if}
    </Row>
</Popover>