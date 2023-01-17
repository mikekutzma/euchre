<script>
  import Hand from "./Hand.svelte";
  import Trick from "./Trick.svelte";
  import Scoreboard from "./Scoreboard.svelte";
  import CallingPickup from "./CallingPickup.svelte";
  import CallingOpen from "./CallingOpen.svelte";
  import Card from "./lib/Card.svelte";
  import { socket, apiUrl, userid } from "./store.js";
  import { get_positions } from "./lib/utils.js";
  import { onMount } from "svelte";

  export let gameData;
  let turn;
  let myTurn = false;
  let trickData;
  let roundState;
  let pickupCard;
  let canPass;
  let numCards = {};

  function getNumCards() {
    const positions = get_positions(gameData);
    let ncards = {};
    for (const player of gameData.players) {
      for (const [position, id] of Object.entries(positions)) {
        if (player.name == id) {
          ncards[position] = player.n_cards;
          break;
        }
      }
    }
    return ncards;
  }

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
      numCards = getNumCards();
    }
  }
</script>

<div class="container">
  <div class="cell status" style="grid-area: status">
    <Scoreboard {gameData} />
  </div>

  {#each ["top", "left", "right"] as position}
    <div class="cell {position}-player" style="grid-area: {position}-player">
      <h3>{get_positions(gameData)[position]}</h3>
      {#each { length: numCards[position] } as _, i}
        <div class="back-card-container">
          <Card cardData={{ back: true }} />
        </div>
      {/each}
    </div>
  {/each}
  <div class="cell bottom-player" style="grid-area: bottom-player">
    <h3>{$userid}</h3>
    <Hand {myTurn} />
  </div>
  <div class="cell mainbox" style="grid-area: mainbox">
    {#if roundState == "CALLING_PICKUP"}
      <CallingPickup {pickupCard} {myTurn} {turn} />
    {:else if roundState == "CALLING_OPEN"}
      <CallingOpen {pickupCard} {myTurn} {turn} {canPass} />
    {:else}
      <Trick {gameData} />
    {/if}
  </div>
</div>

<style>
  .container {
    display: grid;
    width: 100%;
    height: 100%;
    grid-template-columns: 1fr 4fr 1fr;
    grid-template-rows: 1fr 1.5fr 50.5% 1.5fr;
    gap: 10px 10px;
    grid-auto-flow: row;
    grid-template-areas:
      "status status status"
      ". top-player ."
      "left-player mainbox right-player"
      ". bottom-player .";
  }
  .top-player {
    display: flex;
    flex: 1 1 auto;
    justify-content: center;
  }
  .back-card-container {
    max-height: 100px;
  }
  .left-player,
  .right-player {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    justify-content: center;
  }
  .left-player > div,
  .right-player > div {
    transform: rotate(90deg);
    max-height: 70px;
  }
</style>
