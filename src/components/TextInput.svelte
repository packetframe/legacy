<script>
    export let name, placeholder = "";
    export let id;
    export let content = "";
</script>

<main>
    <label>
        <input type="text" name={name} placeholder={placeholder} id={id} bind:value={content}>
    </label>
</main>

<style>
    input {
        border: 1px solid white;
        border-radius: 5px;
        margin: 2px;
        padding: 10px;
        background: transparent;
        color: white;
    }
</style>
