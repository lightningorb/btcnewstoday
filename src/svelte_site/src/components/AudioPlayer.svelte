<script>
  import { onMount } from 'svelte'
  export let src
  let player
  onMount(()=>{
    player.addEventListener('canplay', function() {
      player.play();
      console.log('The audio has finished loading');
    });
  })
</script>

<audio
    class='audio-player'
    bind:this={player}
    {src}
    controls>
    <track kind="captions" />
</audio>
