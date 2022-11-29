<script>
  import { socket, apiUrl } from "./store.js";
  import { onMount } from "svelte";
  import { groupBy } from "lodash-es";

  let lobbyData;
  let players = [];
  let teams = {};
  let teamEntries = [];
  let userData;
  let myTeam;
  let readyToPlay = true;

  $: {
    if (lobbyData) {
      players = lobbyData.players;
      teams = groupBy(players, (player) => player.team);
      teamEntries = Object.entries(teams);
    }
  }

  $: {
    if (userData) {
      myTeam = userData.team;
    }
  }

  $: if ($socket != null) {
    try {
      fetch("http://" + $apiUrl + "/join", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sid: $socket.id }),
      })
        .then((response) => response.json())
        .then((data) => {
          userData = data;
        });
    } catch (err) {
      console.log(err);
    }
  }

  $: if ($socket != null) {
    $socket.on("lobbyUpdate", (data) => {
      console.log("LobbyUpdate: %o", data);
      lobbyData = data;
    });
  }

  function startGame() {
    console.log("Starting game...");
    $socket.emit("startGame", {});
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
