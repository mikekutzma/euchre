import { writable, derived } from "svelte/store";

export const socket = writable();

export const apiUrl = writable("kosh.local:8000");

export const userdata = writable({});

export const userid = derived(userdata, getuserid);

function getuserid(userdata) {
  if (userdata && userdata.username) {
    return userdata.username;
  } else {
    return null;
  }
}
