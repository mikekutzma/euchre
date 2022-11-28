<script>
    import { onMount } from "svelte";
    import { socket, apiUrl} from './store.js';
    import Card from "./Card.svelte";
    export let trickData;
    let trickCards = {};

    $: {
        if (trickData) {
            trickCards = trickData.cards;
        }
    }

</script>

<h1>Trick</h1>
<div class="trick-container">
{#each Object.entries(trickCards) as [player, card]}
    <Card cardData={card} title={player}/>
{/each}
</div>

<style>
    .trick-container {
        flex: 1 1 auto;
    }
    
</style>
