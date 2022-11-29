<script>
  import Hand from "./Hand.svelte";
  import Trick from "./Trick.svelte";
  import Scoreboard from "./Scoreboard.svelte";
  import CallingPickup from "./CallingPickup.svelte";
  import CallingOpen from "./CallingOpen.svelte";
  import { socket, apiUrl, userid } from "./store.js";
  import { onMount } from "svelte";

  export let gameData;
  let turn;
  let myTurn = false;
  let trickData;
  let roundState;
  let pickupCard;
  let canPass;

  $: {
    if (gameData) {
      trickData = gameData.rnd.trick;
      myTurn = gameData.turn == $userid;
      roundState = gameData.rnd.status;
      pickupCard = gameData.rnd.pickup_card;
      canPass = !(
        roundState == "CALLING_OPEN" &&
        gameData.rnd.dealer_index == gameData.turn_index
      );
    }
  }
</script>

<div class="gameboard">
  <Scoreboard {gameData} />

  <div class="board">
    {#if roundState == "CALLING_PICKUP"}
      <CallingPickup {pickupCard} {myTurn} {turn} />
    {:else if roundState == "CALLING_OPEN"}
      <CallingOpen {pickupCard} {myTurn} {turn} {canPass} />
    {:else}
      <Trick {trickData} />
    {/if}

    <Hand {myTurn} />
  </div>
</div>

<style>
  .gameboard {
    display: flex;
    flex-flow: row;
    width: 100%;
    flex: 1 1 auto;
  }

  .board {
    display: flex;
    flex-flow: column;
    flex: 1 1 auto;
  }
</style>
