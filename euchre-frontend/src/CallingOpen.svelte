<script>
  import { socket, gameId } from "./store.js";

  export let pickupCard;
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

<div class="buttonBox">
  {#if myTurn}
    {#each suits as suit}
      <button on:click={() => call(suit)}>
        Call {suit}
      </button>
    {/each}
    {#if canPass}
      <button on:click={pass}>Pass</button>
    {/if}
  {/if}
</div>

<style>
  /*
    .callingContainer {
        display: flex;
    }
    .buttonBox {
        flex: 2;
        height: 100%;
    }
*/
</style>
