<script>
    export let name = "";
    export let id;
    export let content = "";
    export let onchange;
    export let small = false;
    export let large = false;
</script>

<main>
    <label>
        <select bind:value={content} id={id} name={name} on:blur={onchange} class:small class:large>
            <slot/>
        </select>
    </label>
</main>

<style>
    select {
        border: 1px solid white;
        border-radius: 5px;
        margin: 2px;
        color: white;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        padding: 10px 22px 10px 10px;
    }

    .small {
        background: url(https://dash.delivr.dev/img/arrow.png) 96% / 25% no-repeat #000;
    }

    .large {
        background: url(https://dash.delivr.dev/img/arrow.png) 96% / 15% no-repeat #000;
    }
</style>
