<script type="text/javascript">
    import { API_FQDN } from '$lib/constants.js';
    import axios from 'axios';
    import { Popover } from 'sveltestrap';
    export let tweet;
    $: approved = tweet.approved;
    function approve() {
        axios
            .post(API_FQDN + `/api/tweets/approve/${tweet.id}/`)
            .then(function (response) {
                console.log(response);
                approved = true;
            })
            .catch(function (error) {
                console.log(error);
                if (error.response != undefined) {
                    confirm(error.response.data.detail);
                } else {
                    confirm('Error');
                }
            });
    }
</script>

<Popover trigger="hover" target={'id-' + tweet.id} title={'@' + tweet.username}>
    <p>{tweet.text}</p>
</Popover>
{#if approved}
    <a
        rel="noreferrer"
        class={`tweet`}
        id={'id-' + tweet.id}
        target="_blank"
        href={`https://twitter.com/${tweet.username}/status/${tweet.tweet_id}`}>@{tweet.username}</a
    >
{:else}
    <a class={`tweet-pending default-cursor`} id={'id-' + tweet.id} on:click={() => approve()}>@{tweet.username}</a>
{/if}

<span style="width: 3px;" />