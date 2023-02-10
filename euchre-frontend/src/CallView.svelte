<script>
  import Card from "./lib/Card.svelte";
  import { socket, gameId } from "./store.js";

  export let pickupCard;
  export let roundState;
  export let myTurn = false;
  export let canPass = true;
  const allsuits = ["spades", "hearts", "clubs", "diamonds"];
  let suits = [];
  $: suits = allsuits.filter((suit) => suit != pickupCard.suit);

  function call(suit) {
    $socket.emit("callTrump", { suit: suit, gameId: $gameId });
  }

  function pass() {
    $socket.emit("passTrump", { gameId: $gameId });
  }
</script>

<div class="calling-card-container">
  <div class="calling-card-box">
    {#if roundState == "CALLING_PICKUP"}
      <Card cardData={pickupCard} />
    {:else}
      <Card cardData={{ back: true }} />
    {/if}
  </div>
</div>
<div class="call-button-container">
  {#if myTurn}
    {#if roundState == "CALLING_PICKUP"}
      <button on:click={() => call(pickupCard.suit)}>Pickup</button>
    {:else}
      {#each suits as suit}
        <button on:click={() => call(suit)}>
          Call {suit}
        </button>
      {/each}
    {/if}
    {#if canPass}
      <button on:click={pass}>Pass</button>
    {/if}
  {/if}
</div>

<style>
  .call-button-container {
  }
</style>
