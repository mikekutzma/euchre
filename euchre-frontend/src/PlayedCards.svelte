<div class="container">
  <div class="header" />
  <div class="status" />
  <div class="top-player" />
  <div class="left-player" />
  <div class="bottom-player" />
  <div class="right-player" />
  <div class="main" />
</div>

<style>
  .container {
    display: grid;
    grid-template-columns: 1fr 50% 1fr;
    grid-template-rows: 0.5fr 1fr 1.5fr 50.5% 1.5fr;
    gap: 0px 0px;
    grid-auto-flow: row;
    grid-template-areas:
      "header header header"
      "status status status"
      ". top-player ."
      "left-player main right-player"
      ". bottom-player .";
  }

  .header {
    grid-area: header;
  }

  .status {
    grid-area: status;
  }

  .top-player {
    grid-area: top-player;
  }

  .left-player {
    grid-area: left-player;
  }

  .bottom-player {
    grid-area: bottom-player;
  }

  .right-player {
    grid-area: right-player;
  }

  .main {
    grid-area: main;
  }
</style>
