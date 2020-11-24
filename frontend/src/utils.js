import {SnackBars, Debug} from "./stores";

export function addSnackbar(status, message, color, timeout) {
    let id = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
    SnackBars.update(sb => {sb[id] = {status, message, color, timeout}; return sb})
}

export function log(message) {
    if (Debug) {
        console.log(message)
    }
}
