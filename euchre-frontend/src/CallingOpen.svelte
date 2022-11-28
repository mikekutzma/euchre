<script>
    import { socket } from "./store.js";

    export let pickupCard;
    export let myTurn = false;
    export let canPass = true;
    // export let turn;
    let suits = ["spades", "hearts", "clubs", "diamonds"];

    function call(suit){
        $socket.emit("callTrump", {suit});
    }

    function pass(){
        $socket.emit("passTrump", {});
    }

</script>

<div class="buttonBox">
    {#if myTurn}
        {#each suits as suit}
            <button on:click={() => call(suit)}>
                Call {suit}
            </button>
        {/each}
        {#if canPass}
            <button on:click={pass}>Pass</button>
        {/if}
    {/if}
</div>

<style>
/*
    .callingContainer {
        display: flex;
    }
    .buttonBox {
        flex: 2;
        height: 100%;
    }
*/
</style>

