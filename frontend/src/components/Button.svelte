<script>
    export let inverted = false;
    export let color = "white";
    export let icon = "";
    export let disabled = false;
    export let size = ".9rem";
    export let onclick = undefined;
    export let padded = false;
    export let floatRight = false;
    export let centered = false;
    export let type = "button";
    export let tbpadded = false;
    export let rpadded = false;
    export let lpadded = false;
    $: isSlotFilled = $$slots["default"];
</script>

<main>
    <button class:centered class:disabled={disabled} class:float-right={floatRight} class:icon-button={!isSlotFilled} class:inverted class:padded={padded} class:lpadded class:tbpadded class:rpadded disabled={disabled} on:click={onclick} style="--buttonColor:{color}; --fontSize:{size}" type={type}>
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

    .tbpadded {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .rpadded {
        margin-right: 10px;
    }

    .lpadded {
        margin-right: 10px;
    }

    .float-right {
        float: right;
        margin-right: 15px;
    }

    .centered {
        margin: auto;
    }
</style>