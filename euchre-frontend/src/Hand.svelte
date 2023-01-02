<script>
  import { onMount } from "svelte";
  import Card from "./Card.svelte";
  import { socket, apiUrl, gameId } from "./store.js";

  let handCards = [];
  export let myTurn = false;

  async function getHand() {
    try {
      const res = await fetch(
          $apiUrl +
          "/hand?" +
          new URLSearchParams({ gameId: $gameId }),
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

  function playCard(event) {
    if (myTurn) {
      handCards.splice(event.detail.index, 1);
      handCards = handCards; // Needed to react
      $socket.emit("playCard", {
        card: event.detail.card,
        suit: event.detail.suit,
        gameId: $gameId,
      });
    } else {
      alert("Not my turn..");
    }
  }
</script>

<div class="hand-container">
  {#each handCards as card, i}
    <Card on:cardClick={playCard} index={i} cardData={card} />
  {/each}
</div>

<style>
  .hand-container {
    flex: 0 1 auto;
  }
</style>
