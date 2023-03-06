<script>
  import { onMount } from "svelte";
  import Card from "./lib/Card.svelte";
  import { socket, apiUrl, gameId } from "./store.js";

  let handCards = [];
  let roundState;
  export let myTurn = false;
  export let gameData;

  $: {
    if (gameData) {
      roundState = gameData.rnd.status;
    }
  }

  async function getHand() {
    try {
      const res = await fetch(
        $apiUrl + "/hand?" + new URLSearchParams({ gameId: $gameId }),
        {
          credentials: "include",
        }
      );
      const data = await res.json();
      console.log("Hand: %o", data);
      handCards = data;
    } catch (err) {
      console.log(err);
    }
  }

  onMount(getHand);

  $: if ($socket != null) {
    $socket.on("refreshHand", (data) => {
      getHand();
    });
  }

  function playCard(card, ind) {
    console.log("Clicked: index %d card %o", ind, card);
    if (myTurn) {
      handCards.splice(ind, 1);
      handCards = handCards; // Needed to react
      console.log("New Hand: %o", handCards);
      if (roundState == "PLAYING") {
        $socket.emit("playCard", {
          card: card,
          gameId: $gameId,
        });
      } else if (roundState == "PICKUP_DISCARD") {
        $socket.emit("discardCard", {
          card: card,
          gameId: $gameId,
        });
      }
    }
  }
</script>

<div class="upright-player hand-cards-container">
  {#each handCards as card, i (card)}
    <div
      class="click-container upright-card-box"
      on:click={() => playCard(card, i)}
    >
      <Card cardData={card} />
    </div>
  {/each}
</div>

<style>
</style>
