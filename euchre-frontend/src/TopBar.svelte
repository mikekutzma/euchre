<script>
  import { apiUrl, userdata } from "./store.js";
  import { onMount } from "svelte";

  let username;

  async function setUserData() {
    try {
      const res = await fetch($apiUrl + "/getSession", {
        credentials: "include",
      });
      const data = await res.json();

      username = data.username;
      userdata.set(data);
    } catch (err) {
      console.log(err);
    }
  }

  onMount(setUserData);

  function open_settings() {
    console.log("Open Settings Soon...");
    return;
  }
</script>

<div class="top-bar header">
  <button class="username-button" type="button" on:click={open_settings}>
    {username}
  </button>
</div>

<style>
  .top-bar {
    flex: 0 1 auto;
    background-color: #333;
    display: flex;
    justify-content: left;
  }

  .username-button {
    font-weight: bold;
  }
</style>
