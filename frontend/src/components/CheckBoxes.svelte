<script>
    export let nodes = [];
</script>

<main>
    {#each nodes as node}
        <div class="container">
            <label class="capital">
                <input type="checkbox" id="{node['name']}" name="{node['name']}" value="{node['name']}">
                {node['name'].toUpperCase()}
            </label>
        </div>
    {/each}
</main>

<style>

    .container {
        color: white;
        margin: 1px;
        width: 100%;
    }

    label {
        padding: 2px 10px 2px 10px;
        border-radius: 15px;
        transition: ease background-color 0.3s;
        display: flex;
    }

    label:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    label:active {
        background-color: rgba(255, 255, 255, 0.4);
        margin-left: 2px;
    }

    input {
        padding: 0px;
        margin: 2px 5px 2px 2px;
    }

    main {
        margin: 0;
        width: 100%;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
    }

</style>
