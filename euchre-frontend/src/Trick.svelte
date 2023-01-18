<script>
  import { onMount } from "svelte";
  import { socket, apiUrl } from "./store.js";
  import Card from "./lib/Card.svelte";
  import { get_positions } from "./lib/utils.js";

  export let gameData;
  export let trickCards = {};
  let cards = { top: null, left: null, right: null, bottom: null };
  let positions = {};

  $: {
    if (gameData) {
      trickCards = gameData.rnd.trick.cards;

      positions = get_positions(gameData);
      for (const [position, name] of Object.entries(positions)) {
        cards[position] = trickCards[name];
      }
    }
  }
</script>

<div class="container">
  {#each Object.keys(cards) as position}
    <div class="card-cell" style="grid-area: {position}-card-cell">
      {#if cards[position]}
        <Card cardData={cards[position]} />
      {/if}
    </div>
  {/each}
</div>

<style>
  .container {
    display: grid;
    height: 100%;
    width: 100%;
    justify: center;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    gap: 10px 4px;
    grid-auto-flow: row;
    grid-template-areas:
      ". top-card-cell ."
      "left-card-cell . right-card-cell"
      ". bottom-card-cell .";
  }

  .card-cell {
    max-height: 100px;
  }
</style>
