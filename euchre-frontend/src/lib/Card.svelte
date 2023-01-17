<script>
  export let cardData;

  function getImagePath(data) {
    const dir = "cards/";
    let path;
    if (data.back == true) {
      path = dir + "blue_back" + ".png";
    } else {
      path = dir + data.number + "_of_" + data.suit + ".png";
    }
    return path;
  }

  const src = getImagePath(cardData);
</script>

  {#if cardData.back}
    <img {src} alt="Card Back" />
  {:else}
    <img {src} alt="{cardData.number} of {cardData.suit}" />
  {/if}

<style>
  .card {
    display: inline-block;
    width: 100%;
    height: 100%;
    
  }

  img {
    width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
</style>
