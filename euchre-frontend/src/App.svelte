<script>
  import TopBar from "./TopBar.svelte";
  import GameContainer from "./GameContainer.svelte";
  import { io } from "socket.io-client";
  import { socket, socketUrl } from "./store.js";

  $socket = io($socketUrl);
</script>

<TopBar />
<GameContainer />

<style>
</style>
