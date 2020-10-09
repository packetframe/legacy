import {SnackBars} from "./stores";

export function addSnackbar(status, message, color, timeout) {
    let id = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
    $SnackBars[id] = {status, message, color, timeout}
}