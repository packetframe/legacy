import {writable} from "svelte/store";

export const SnackBars = writable({});
export let Page = writable("index");
export let IsAdmin = writable(false);