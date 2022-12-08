<script text='text/javascript'>
    import { preferences } from '$lib/store.js';
    import { Icon } from 'sveltestrap';
    import { get } from 'svelte/store';
    export let podcast = null;

    let url = podcast.link;
    $: has_audio = url.includes('.mp3');

    function play() {
      let p = get(preferences);
      p.podcast = url;
      preferences.set(p);
    }
</script>
{#if has_audio}
    <button class={'play-button'} on:click={play}><Icon name='play'/></button>
{/if}
