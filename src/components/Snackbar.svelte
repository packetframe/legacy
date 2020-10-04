<script>
    export let open = false;
    export let status = "200";
    export let message = "";
    export let color = "green";
    export let handleClose = () => {console.log('You need a function here!')};
    export let timeout = 4000;
    export let grouped = false;

    import {fly} from 'svelte/transition'
    import { sineInOut } from 'svelte/easing'
    import { onMount } from 'svelte'

    onMount(() => {
        if (grouped) {
            open = true;
            handleClose = () => {open = false;}
        }

        let autoClose = setTimeout(handleClose, timeout);

        return () => {clearTimeout(autoClose);}
    })

    // example usage:
    // <Snackbar
    //      color="green"
    //      status="200"
    //      message="Successfully added snackbar."
    //      handleClose={() => {open = false}}      <---- handleClose must always evaluate the var to false.
    // />

</script>

{#if open}
    <main
            transition:fly="{{delay: 50, duration: 400, y:100, easing: sineInOut }}" style="--mainColor:{color};"
            class:grouped={grouped} class:ungrouped={!grouped}
    >
        <p>{status}</p>
        <p>{message}</p>
        <span class="material-icons" on:click={handleClose}>
        close
    </span>
    </main>
{/if}

<style>
    main.ungrouped {
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
    main.grouped {
        color: white;
        background: var(--mainColor);
        border-radius: 5px;
        display: flex;
        align-items: center;
        overflow: hidden;
        margin: 2px;
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
    :global(.snackbar) {
        color: white;
    }
</style>