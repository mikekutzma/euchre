<script>
  import GameBoard from "./GameBoard.svelte";
  import Lobby from "./Lobby.svelte";
  import { socket, apiUrl, gameId } from "./store.js";
  import { onMount } from "svelte";

  let isLive = false;
  let inGame = false;
  let gameData;
  let gamesData = [];
  let gameId_holder;

  $: {
    if (gameData) {
      isLive = gameData.live;
      inGame = true;
    }
  }
  $: {
      if (gameId_holder) {
          $gameId = gameId_holder;
      }
  }

  async function join(gameId) {
    try {
      const res = await fetch($apiUrl + "/join", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          gameId: gameId,
          sid: $socket.id,
        }),
      });
      const data = await res.json();
      gameData = data;
      gameId_holder = gameData.game_id;
    } catch (err) {
      console.log(err);
    }
  }

  async function getGameStatus() {
    try {
      const res = await fetch($apiUrl + "/gameStatus");
      const data = await res.json();
      console.log("Initial Game Status: %o", data);
      gameData = data;
    } catch (err) {
      console.log(err);
    }
  }

  async function getGames() {
    try {
      const res = await fetch($apiUrl + "/games?live=0");
      const data = await res.json();
      console.log("Games: %o", data);
      gamesData = data;
    } catch (err) {
      console.log(err);
    }
  }

  async function newGame() {
    try {
      const res = await fetch($apiUrl + "/newGame", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      console.log(data);
      const gameId = data["gameId"];
      return gameId;
    } catch (err) {
      console.log(err);
    }
  }

  async function joinNewGame() {
    const game_id = await newGame();
    join(game_id);
  }

  // onMount(getGameStatus);
  onMount(getGames);

  $: if ($socket != null) {
    $socket.on("gameStatus", (data) => {
      console.log("Game Status Update: %o", data);
      gameData = data;
    });

    $socket.on("gamesUpdate", (data) => {
      console.log("Games Update: %o", data);
      gamesData = data;
    });
  }
</script>

{#if isLive}
  <GameBoard {gameData} />
{:else if inGame}
  <Lobby {gameData} />
{:else}
  <div class="new-game-container">
    <button class="new-game-button" on:click={joinNewGame}> New Game </button>
  </div>
  <div class="games-container">
    {#each gamesData as game}
      <div class="game-container">
        {game}
        <button on:click={() => join(game)}>Join</button>
      </div>
    {/each}
  </div>
{/if}

<style>
  .games-container {
    display: flex;
    flex-direction: column;
  }

  .game-container {
    border: 1px solid gray;
  }
</style>
