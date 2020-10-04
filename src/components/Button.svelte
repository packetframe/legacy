<script>
    export let inverted = false;
    export let color = "white";
    export let icon = "";
    export let disabled = false;
    export let size = ".9rem";
    export let onclick = undefined;
    export let padded = false;
    export let floatRight = false;
    $: isSlotFilled = $$slots["default"];
</script>

<main>
    <button class:padded={padded} class:inverted style="--buttonColor:{color}; --fontSize:{size}" class:icon-button={!isSlotFilled} disabled={disabled} class:disabled={disabled} on:click={onclick} class:float-right={floatRight}>
        {#if icon !== ""}
        <span class="material-icons" class:icon-button-icon={!isSlotFilled}>
            {icon}
        </span>
        {/if}

        {#if isSlotFilled}
            <div>
                <slot></slot>
            </div>
        {/if}
    </button>
</main>

<style>
    button {
        background: transparent;
        color: var(--buttonColor);
        display: flex;
        align-items: center;
        border-radius: 25px;
        border-style: solid;
        border-color: var(--buttonColor);
        border-width: 2px;
        opacity: 0.6;
        transition: 0.3s;
        font-size: var(--fontSize);
        margin: 0px;
        padding: 0px 5px 0px 5px;
    }

    button:active {
        transform: scale(93%, 93%);
    }

    .disabled:active {
        transform: none;
    }

    button > span {
        color: inherit;
        padding-left: 5px;
        font-size: calc(var(--fontSize) + 0.2rem);
    }

    button div {
        margin: 10px;
    }

    button div:active {
        margin: 10px;
    }

    .icon-button-icon {
        padding: 0px;
        font-size: calc(var(--fontSize) + 0.2rem);
    }

    .icon-button {
        padding: 8px;
        border-radius: 50px;
    }

    .inverted {
        background-color: var(--buttonColor);
        color: black;
        opacity: 1;
    }

    .material-icons {
        /* background-color: transparent !important; */
    }

    button:hover {
        opacity: 1;
    }

    .inverted:hover {
        background-color: transparent;
        color: var(--buttonColor);
    }

    .disabled:hover {
        opacity: 0.6;
    }

    .inverted.disabled:hover {
        background-color: var(--buttonColor);
        color: black;
        opacity: 1;
    }

    .padded {
        margin: 10px;
    }

    .float-right {
        float: right;
        margin-right: 15px;
    }
</style>