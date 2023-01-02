<script>
  import TopBar from "./TopBar.svelte";
  import GameContainer from "./GameContainer.svelte";
  import { io } from "socket.io-client";
  import { socket, socketUrl } from "./store.js";
  import { onMount } from "svelte";

  let isAuthenticated = false;

  $socket = io($socketUrl);

  function login(event) {
    isAuthenticated = true;
  }

  function logout(event) {
    isAuthenticated = false;
  }
</script>

<TopBar {isAuthenticated} on:login={login} on:logout={logout} />
{#if isAuthenticated}
  <GameContainer />
{/if}

<style>
</style>
