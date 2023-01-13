<script>
    import { role_is_at_least } from '$lib/utils.js';
    import { Popover } from 'sveltestrap';
    import axios from 'axios';
    import { API_FQDN } from '$lib/constants.js';
    export var note;
    $: approved = note.approved;
    function approve() {
        axios
            .post(API_FQDN + `/api/notes/approve/${note.id}/`)
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

<Popover trigger="hover" target={'id-' + note.note_id} title={'@' + note.username}>
    <p>{note.text}</p>
</Popover>
{#if approved}
    <a
        rel="noreferrer"
        class={`tweet`}
        id={'id-' + note.note_id}
        target="_blank"
        href="https://astral.ninja/{note.note_id}">@{note.username}</a
    >
{:else}
    <a class={`tweet-pending default-cursor`} id={'id-' + note.note_id} on:click={() => approve()}>@{note.username}</a>
{/if}
<span style="width: 3px;" />