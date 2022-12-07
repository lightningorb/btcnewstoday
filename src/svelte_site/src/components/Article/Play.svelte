<script text='text/javascript'>
    import { Icon } from 'sveltestrap';
    import axios from 'axios';
    import { onMount } from 'svelte';

    $: is_playing = 0;
    $: icons = ['play', 'pause'];
    export let podcast = null;

    let audio = null;
    let url = podcast.link;
    $: has_audio = url.includes('.mp3');

    function play() {
      if (audio == null) {
        audio = new Audio(url);
      }
      if (is_playing == 0) {
        audio.play();
      } else {
        audio.pause();
      }
      is_playing = is_playing == 0 ? 1 : 0;
    }
</script>
{#if has_audio}
    <button class={is_playing == true ? 'pause-button' : 'play-button'} on:click={play}><Icon name={icons[is_playing]}/></button>
{/if}
