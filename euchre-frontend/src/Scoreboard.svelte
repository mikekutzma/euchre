<script>
    import { socket } from "./store.js";
    export let gameData;
    let scores = [0, 0];
    let turn;
    let winner;
    let trump;
    let led;
    let rnd;
    let trick;

    $: {
        if (gameData) {
            scores = gameData.score;
            // turn = gameData.trick.turn;
            trump = gameData.rnd.trump;
            winner = null;
            if (gameData.rnd.trick.winner) {
                winner = gameData.rnd.trick.winner.name;
            }
            led = gameData.rnd.trick.led;
            rnd = gameData.rnd;
            trick = rnd.trick;
        }
    }

    function clearTrick() {
        console.log("Clearing Trick");
        $socket.emit("clearTrick", {});
    }

    function startRound() {
        console.log("Starting Round");
        $socket.emit("startRound", {});
    }

</script>

<div class="scoresContainer">
    <div class="scorediv">
        <span>{scores[0]}</span>
    </div>
    <pre id="statusdump">
        {JSON.stringify(gameData, undefined, 2)}
    </pre>
    <div class="scoresmiddle">
        
    {#if trump}
        <span>Trump: {trump}</span>
    {/if}

    {#if winner}
        <span>Winner: {winner}</span>
    {/if}

    {#if rnd.done}
        <button on:click={startRound}>Start Round</button>
    {:else if trick.done}
        <button on:click={clearTrick}>Clear Trick</button>
    {/if}


        
    </div>
    <div class="scorediv">
        <span>{scores[1]}</span>
    </div>
</div>
<style>
    #statusdump {
        font-size: 0.4em;
        text-align: left;
    }
    .scoresContainer{
        display: flex;
        flex-flow: row;
        flex: 0 1 300px;
        border: 1px solid white;
        font-size: 2em;
        overflow:auto;
        height: 100vh;
    }

    .scorediv {
    }

    .scoresmiddle {
        flex-grow: 8;
    }
</style>
