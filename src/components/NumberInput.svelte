<script>
    export let name, placeholder = "";
    export let id;
    export let content = "";
</script>

<main>
    <label>
        <input bind:value={content} id={id} name={name} placeholder={placeholder} type="number">
    </label>
</main>

<style>
    main {
        width: calc(100% - 25px);
    }

    input {
        border: 1px solid white;
        border-radius: 5px;
        margin: 2px;
        padding: 10px;
        background: transparent;
        color: white;
        width: 100%;
    }
</style>
