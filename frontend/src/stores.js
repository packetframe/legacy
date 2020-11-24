import {writable} from "svelte/store";

export const SnackBars = writable({});
export let IsAdmin = writable(false);
export let Debug = writable(true);
export let API = writable("https://dash.delivr.dev/api/");
