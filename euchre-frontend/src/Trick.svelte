<script>
  import { onMount } from "svelte";
  import { socket, apiUrl } from "./store.js";
  import Card from "./lib/Card.svelte";
  export let trickData;
  export let players = [];
  let trickCards = {};

  $: {
    if (trickData) {
      trickCards = trickData.cards;
    }
  }
</script>

{#each players as player}
  <div class="trick-{player.position}-container trick-cell">
    {#if trickCards[player.name]}
      <div class="trick-card-box">
        <Card cardData={trickCards[player.name]} />
      </div>
    {/if}
  </div>
{/each}

<style>
</style>
