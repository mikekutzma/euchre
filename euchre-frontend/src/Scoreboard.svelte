<script>
  import { socket, gameId } from "./store.js";
  export let gameData;
  let teams = [];

  function getteams(data) {
    let teams = [
      { players: [], score: data.score[0] },
      { players: [], score: data.score[1] },
    ];
    data.players.forEach((player) => {
      teams[player.team].players.push(player.name);
    });
    teams.forEach((team) => {
        team.name = [...team.players].sort().join(" & ");
    });
    return teams;
  }

  $: {
    if (gameData) {
      teams = getteams(gameData);
    }
  }
</script>

<div class="scoreboard">
  <div class="score-box">
    {#each teams as team}
      <div class="team-score-box">
        <div class="team-name">{team.name}</div>
        <div class="team-score">{team.score}</div>
      </div>
    {/each}
  </div>
</div>

<style>
  .scoreboard {
    border-radius: 30px;
    margin: 5px;
    padding: 10px;
  }

  .score-box {
  }

  .team-score-box {
    display: flex;
    justify-content: space-between;
  }
</style>
