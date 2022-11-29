<script>
  import { apiUrl, userdata } from "./store.js";
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let username;
  export let isAuthenticated = false;

  async function setUserData() {
    try {
      const res = await fetch("http://" + $apiUrl + "/getSession");
      const data = await res.json();
      // const data = {logged_in: true, username: "Mike"};

      if (data.logged_in == true) {
        isAuthenticated = true;
        username = data.username;
        userdata.set(data);
        dispatch("login");
      } else {
        isAuthenticated = false;
        dispatch("logout");
      }
    } catch (err) {
      console.log(err);
    }
  }

  onMount(setUserData);

  async function login() {
    if (!username) {
      return;
    }
    try {
      const res = await fetch("http://" + $apiUrl + "/login", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username }),
      });
      const data = await res.json();
      setUserData();
    } catch (err) {
      console.log(err);
    }
  }

  const logout = () => {
    fetch("http://" + $apiUrl + "/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        isAuthenticated = false;
        username = null;
        dispatch("logout");
      })
      .catch((err) => {
        console.log(err);
      });
  };
</script>

<div class="top-bar">
  {#if isAuthenticated}
    <div class="LeftBox">
      <strong>
        {username}
      </strong>
    </div>
    <button type="button" on:click={logout}>Log Out</button>
  {:else}
    <form id="form" on:submit|preventDefault={login}>
      <div class="LeftBox">
        <input type="text" placeholder="username" bind:value={username} />
      </div>
      <button type="button" on:click={login}>login</button>
    </form>
  {/if}
</div>

<style>
  .top-bar {
    flex: 0 1 auto;
    background-color: #333;
    display: flex;
    justify-content: left;
  }

  .top-bar form {
    display: flex;
    justify-content: left;
  }

  .LeftBox {
    width: 150px;
    text-align: center;
    display: inline-block;
    vertical-align: middle;
    padding: 10px 0;
    font-size: 1.5em;
  }
</style>
