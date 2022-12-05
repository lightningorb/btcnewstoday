<script text='text/javascript'>
    import { Icon } from 'sveltestrap';
    import axios from 'axios';
    import { onMount } from 'svelte';

    $: is_playing = 0;
    $: icons = ['play', 'pause'];
    $: has_audio = false;
    export let article;

    let audio = null;
    let url = `https://btcnewstoday.s3.us-east-2.amazonaws.com/${article.id}.mp4`;

    async function checkURL(url){
      try {
        const response = await axios.get(url);
        has_audio = true;
        
      } catch (error) {
        if (error.response.status === 404) {
          // console.log(`${url} returned a 404 error!`);
        } else {
          // console.log(`An error occurred while checking ${url}: ${error}`);
        }
      }
    }

    onMount(async () => {
      checkURL(url)
    });

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
