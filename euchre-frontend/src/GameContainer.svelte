<script>
  import GameBoard from "./GameBoard.svelte";
  import Lobby from "./Lobby.svelte";
  import { socket, apiUrl } from "./store.js";
  import { onMount } from "svelte";

  let isLive = false;
  let gameData;

  $: {
    if (gameData) {
      isLive = gameData.live;
    }
  }

  async function getGameStatus() {
    try {
      const res = await fetch("http://" + $apiUrl + "/gameStatus");
      const data = await res.json();
      console.log("Initial Game Status: %o", data);
      gameData = data;
    } catch (err) {
      console.log(err);
    }
  }

  onMount(getGameStatus);

  $: if ($socket != null) {
    $socket.on("gameStatus", (data) => {
      console.log("Game Status Update: %o", data);
      gameData = data;
      $socket.emit("gameStatus_mimic", data);
    });
  }
</script>

{#if isLive}
  <GameBoard {gameData} />
{:else}
  <Lobby />
{/if}

<style>
</style>
