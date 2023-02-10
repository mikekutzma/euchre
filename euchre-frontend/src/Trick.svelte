<script>
  import { onMount } from "svelte";
  import { socket, gameId } from "./store.js";
  import Card from "./lib/Card.svelte";
  export let gameData;
  export let players = [];
  let trickCards = {};

  $: {
    if (gameData) {
      trickCards = gameData.rnd.trick.cards;
    }
  }
  function clearTrick() {
    console.log("Clearing Trick");
    $socket.emit("clearTrick", { gameId: $gameId });
  }

  function startRound() {
    console.log("Starting Round");
    $socket.emit("startRound", { gameId: $gameId });
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

<div class="trick-center-container trick-cell">
  {#if gameData.rnd.done}
    <button on:click={startRound}>Start Round</button>
  {:else if gameData.rnd.trick.done}
    <button on:click={clearTrick}>Clear Trick</button>
  {/if}
</div>

<style>
  button {
    display: inline-block;
    max-height: 30%;
  }
  .trick-center-container {
    display: flex;
    align-items: center;
  }
</style>
