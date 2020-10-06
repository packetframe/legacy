<script>
    export let name, placeholder = "";
    export let id;
    export let content = "";
    export let password = false;
</script>

<main>
    <!-- This is to get around svelte's limitation of limiting dynamic type attributes if the input uses two-way binding -->
    {#if password}
        <input bind:value={content} id={id} name={name} placeholder={placeholder} type="password">
    {:else}
        <input bind:value={content} id={id} name={name} placeholder={placeholder} type="text">
    {/if}
</main>

<style>
    input {
        border: 1px solid white;
        border-radius: 5px;
        margin: 2px;
        padding: 10px;
        background: transparent;
        color: white;
        width: calc(100% - 25px);
    }
</style>
