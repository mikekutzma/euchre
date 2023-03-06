<script>
  import Hand from "./Hand.svelte";
  import Trick from "./Trick.svelte";
  import Card from "./lib/Card.svelte";
  import { getPlayersData } from "./lib/utils.js";
  import Scoreboard from "./Scoreboard.svelte";
  import CallView from "./CallView.svelte";
  import { socket, apiUrl, userid } from "./store.js";
  import { onMount } from "svelte";

  export let gameData;
  let turn;
  let myTurn = false;
  let trickData;
  let roundState;
  let pickupCard;
  let canPass;
  let players = [];

  $: {
    if (gameData) {
      players = getPlayersData(gameData, $userid);
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

<div class="live-game-container">
  <Scoreboard {gameData} />
  {#each players as player}
    <div class="{player.position}-player-container hand-container">
      <div class="name-container">
        <strong>
          {player.name}
        </strong>
      </div>
      {#if player.name == $userid}
        <Hand {myTurn} {gameData} />
      {:else}
        <div class="{player.orientation}-player hand-cards-container">
          {#each { length: player.n_cards } as _, i}
            <div class="{player.orientation}-card-box">
              <Card
                cardData={{ back: true, rotate: player.orientation == "side" }}
              />
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/each}

  {#if roundState == "PLAYING"}
    <div class="board-center-container trick-container">
      <Trick {gameData} {players} />
    </div>
  {:else}
    <div class="board-center-container call-view-container">
      <CallView {pickupCard} {myTurn} {canPass} {roundState} />
    </div>
  {/if}
</div>

<style>
</style>
