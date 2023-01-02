<script>
  import Card from "./Card.svelte";
  import { socket, gameId } from "./store.js";

  export let pickupCard;
  export let myTurn = false;
  // export let turn;

  function call() {
    $socket.emit("callTrump", { suit: pickupCard.suit , gameId: $gameId });
  }

  function pass() {
    $socket.emit("passTrump", {gameId: $gameId});
  }
</script>

<div class="callingContainer">
  <Card cardData={pickupCard} />
  <div class="buttonBox">
    {#if myTurn}
      <button on:click={call}>Call</button>
      <button on:click={pass}>Pass</button>
    {/if}
  </div>
</div>

<style>
  .callingContainer {
    flex: 1 1 auto;
  }
  /*
    .buttonBox {
        flex: 2;
        height: 100%;
    }
*/
</style>
