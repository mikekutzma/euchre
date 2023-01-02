<script>
  import { socket, apiUrl, gameId } from "./store.js";
  import { onMount } from "svelte";
  import { groupBy } from "lodash-es";

  export let gameData;
  let players = [];
  let teams = {};
  let teamEntries = [];
  let readyToPlay = true;

  $: {
    if (gameData) {
      players = gameData.players;
      teams = groupBy(players, (player) => player.team);
      teamEntries = Object.entries(teams);
    }
  }

  $: if ($socket != null) {
    $socket.on("lobbyUpdate", (data) => {
      console.log("LobbyUpdate: %o", data);
      gameData = data;
    });
  }

  function startGame() {
      console.log("Starting game with id: "+$gameId+"...");
    $socket.emit("startGame", { gameId: $gameId });
  }
</script>

<h1>Lobby</h1>
{#if readyToPlay}
  <button on:click={startGame}> Start Game </button>
{/if}
<ul>
  {#each teamEntries as [team, teamPlayers]}
    <li>
      {team}
      <ul>
        {#each teamPlayers as player}
          <li>
            {player.name}
          </li>
        {/each}
      </ul>
    </li>
  {/each}
</ul>
