import { writable, derived } from "svelte/store";

export const socket = writable();

export const apiUrl = writable(import.meta.env.VITE_API_URL);
export const socketUrl = writable(import.meta.env.VITE_SOCKET_URL);

export const userdata = writable({});

export const gameId = writable();

export const userid = derived(userdata, getuserid);

function getuserid(userdata) {
  if (userdata && userdata.username) {
    return userdata.username;
  } else {
    return null;
  }
}
