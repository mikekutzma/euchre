<script>
  export let cardData;
  function getImagePath(data) {
    const dir = "cards/";
    let path = dir;
    if (data.back == true) {
      path = path + "blue_back";
    } else {
      path = path + data.number + "_of_" + data.suit;
    }
    if (data.rotate == true) {
      path = path + "_rot";
    }
    path = path + ".png";
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
  img {
    width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
</style>
