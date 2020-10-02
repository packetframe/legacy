<script>
    import {fly} from 'svelte/transition'
    import { sineInOut } from 'svelte/easing'

    export let open = false;
    export let status = "200";
    export let message = "";
    export let color = "green";
    export let handleClose = () => {
        console.log('You need a function here!')
    };
    export let timeout = 4000;

    let autoClose;

    $: if (open) {
        autoClose = setTimeout(handleClose, timeout)
    } else {
        clearTimeout(autoClose)
    }
</script>

{#if open}
    <main transition:fly="{{delay: 50, duration: 400, y:100, easing: sineInOut }}" style="--mainColor:{color}">
        <p>{status}</p>
        <p>{message}</p>
        <span class="material-icons" on:click={handleClose}>
        close
    </span>
    </main>
{/if}

<style>
    main {
        color: white;
        background: var(--mainColor);
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translatex(-50%);
        border-radius: 5px;
        display: flex;
        align-items: center;
    }

    p {
        margin: 10px;
    }

    span {
        font-size: 18px;
        margin: 10px;
        background: rgba(255, 255, 255, 0.5);
        color: white;
        border-radius: 25px;
        padding: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    span:hover {
        background: rgba(255, 255, 255, 0.4);
        cursor: pointer;
    }
</style>