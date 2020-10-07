import {writable} from "svelte/store";

export const SnackBars = writable({});
export let APIKey = writable({});
export let Page = writable("login");
export let IsAdmin = writable(false);