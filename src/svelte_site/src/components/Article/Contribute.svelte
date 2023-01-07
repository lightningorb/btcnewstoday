<script type="text/javascript">
    import { preferences } from '$lib/store.js';
    import { API_FQDN } from '$lib/constants.js';
    import { onMount } from 'svelte';
    import { role_is_at_least } from '$lib/utils.js';
    import { Input, Icon } from 'sveltestrap';
    import { Popover } from 'sveltestrap';

    import { Col, Container, Row } from 'sveltestrap';
    import AddTweet from './AddTweet.svelte';
    import AddNostrNote from './AddNostrNote.svelte';
    import { Button } from 'sveltestrap';
    import axios from 'axios';
    export let mouseover;
    export let article;
    export let edit;
    function on_click(){
        edit = true;
    }
    let bounty_data = null;
    let isOpen = false;
    let can_add_tweet = false;
    let can_add_note = false;
    let sats_for_tweet = false;
    let sats_for_note = false;
    let note_bounty = 0;
    let tweet_bounty = 0;
    let is_contributor = role_is_at_least('contributor');
    onMount(() => {
        if (!is_contributor)
            return
        axios
            .get(`${API_FQDN}/api/bounty/?article_id=${article.id}`) // , body, { headers: headers }
            .then(function (response) {
                can_add_note = response.data.can_add_note;
                can_add_tweet = response.data.can_add_tweet;
                sats_for_note = response.data.sats_for_note;
                sats_for_tweet = response.data.sats_for_tweet;
                note_bounty = response.data.note_bounty;
                tweet_bounty = response.data.tweet_bounty;
            })
            .catch(function (error) {
                console.log(error);
            });
    });
</script>

{#if is_contributor}
    {#if can_add_tweet || can_add_note}
        <Icon id={`btn-ctrl-${article.id}`} style="padding-left: 5px; font-size: 0.8em;" name="plus-circle"/>
        {#if sats_for_tweet || sats_for_note}
            <span class='dorrar'>$</span>
        {/if}

        <div class="mt-3">
          <Popover
            bind:isOpen
            placement="right"
            target={`btn-ctrl-${article.id}`}
            style='width: 150px;'
          >
            <Row>
                {#if role_is_at_least('editor')}
                    <div><button style='border: 0;' on:click={on_click}><Icon name="pencil-square" /></button> Edit</div>
                {/if}
                {#if can_add_tweet}
                    <AddTweet bind:isOpen={isOpen} tweet_bounty={tweet_bounty} sats_for_tweet={sats_for_tweet} article_id={article.id}/><br />
                {/if}
                {#if can_add_note}
                    <AddNostrNote bind:isOpen={isOpen} note_bounty={note_bounty} sats_for_note={sats_for_note} article_id={article.id}/><br />
                {/if}
            </Row>
          </Popover>
        </div>
    {/if}
{:else}
{#if $preferences.show_bounties}
    <span on:mouseover={() => mouseover = true} id={`btn-pop-${article.id}`} class='grey-dorrar'>$</span>
    <div class="mt-3">
      <Popover
        bind:mouseover
        target={`btn-pop-${article.id}`}
        placement="left"
      >
        Add tweets <Icon name="twitter"/> / notes <img src="/add-nostr-note.png" style="width: 14px;" />.<br/><a href='/dashboard/login'>login</a>
      </Popover>
    </div>
{/if}
{/if}