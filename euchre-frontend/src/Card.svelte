<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  export let cardData;
  export let index;
  export let title;
  let src;

  function getImagePath(num, suit) {
    return "cards/" + num + "_of_" + suit + ".png";
  }

  $: if (cardData) {
    // num = cardData.number.split("_")[1].toLowerCase();
    // suit = cardData.suit.split("_")[1].toLowerCase();
    src = getImagePath(cardData.number, cardData.suit);
  }

  function cardClick() {
    dispatch("cardClick", { card: cardData, index: index });
  }
</script>

<div class="card-container" on:click={cardClick}>
  {#if title}
    <h3>{title}</h3>
  {/if}
  <img {src} alt="{cardData.number} of {cardData.suit}s" />
</div>

<style>
  .card-container {
    display: inline-block;
    width: 10%; /* you can use % */
    padding: 1px;
  }

  img {
    width: 100%; /* you can use % */
    height: auto;
  }
</style>
