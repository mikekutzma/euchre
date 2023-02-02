export function getPlayersData(data, id) {
  const NPLAYERS = 4;
  const positions = [
    { position: "bottom", orientation: "upright" },
    { position: "left", orientation: "side" },
    { position: "top", orientation: "upright" },
    { position: "right", orientation: "side" },
  ];
  let own_index = data.players
    .map(function (e) {
      return e.name;
    })
    .indexOf(id);

  let playersdata = [];
  for (let i = 0; i < NPLAYERS; i++) {
    let playerdata = {
      ...positions[i],
      ...data.players[(i + own_index) % NPLAYERS],
    };
    playersdata.push(playerdata);
  }
  return playersdata;
}
