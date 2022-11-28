<script>
    import TopBar from "./TopBar.svelte";
    import GameContainer from "./GameContainer.svelte"
    import { io } from "socket.io-client";
    import { socket, apiUrl} from "./store.js";
    import { onMount} from "svelte"

    let isAuthenticated = false;

    $socket = io("ws://"+$apiUrl);

    function login(event) {
        isAuthenticated = true;
    }

    function logout(event) {
        isAuthenticated = false;
    }

    
</script>

<TopBar isAuthenticated={isAuthenticated} on:login={login} on:logout={logout}/>
{#if isAuthenticated}
    <GameContainer/>
{/if}

<style>


</style>
