<script>
    export let name = "";
    export let id;
    export let content = "";
    export let onchange;
</script>

<main>
    <label>
        <select bind:value={content} id={id} name={name} on:blur={onchange}>
            <slot/>
        </select>
    </label>
</main>

<style>
    select {
        border: 1px solid white;
        border-radius: 5px;
        margin: 2px;
        padding: 10px;
        color: white;
        background: url(https://dash.delivr.dev/img/arrow.png) 96% / 25% no-repeat #000;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
    }
</style>
