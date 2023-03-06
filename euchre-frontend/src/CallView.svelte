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
    if (roundState == "CALLING_PICKUP") {
      $socket.emit("callTrumpPickup", { suit: suit, gameId: $gameId });
    } else {
      $socket.emit("callTrumpOpen", { suit: suit, gameId: $gameId });
    }
  }

  function pass() {
    $socket.emit("passTrump", { gameId: $gameId });
  }
</script>

<!-- Probably we can clean this up to move the if out so
     we can center the discard message -->
<div class="calling-card-container">
  <div class="calling-card-box">
    {#if roundState == "CALLING_PICKUP"}
      <Card cardData={pickupCard} />
    {:else if roundState == "CALLING_OPEN"}
      <Card cardData={{ back: true }} />
    {:else if roundState == "PICKUP_DISCARD"}
      <!-- Show no card for pickup -->
    {/if}
  </div>
</div>
<div class="call-button-container">
  {#if myTurn}
    {#if roundState == "CALLING_PICKUP"}
      <button on:click={() => call(pickupCard.suit)}>Pickup</button>
      {#if canPass}
        <button on:click={pass}>Pass</button>
      {/if}
    {:else if roundState == "CALLING_OPEN"}
      {#each suits as suit}
        <button on:click={() => call(suit)}>
          Call {suit}
        </button>
      {/each}
      {#if canPass}
        <button on:click={pass}>Pass</button>
      {/if}
    {:else}
      <i>Discard one card</i>
    {/if}
  {/if}
</div>

<style>
  .call-button-container {
  }
</style>
